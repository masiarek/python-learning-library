//! How long is a string? There are at least four answers, and wc knows three.
//!
//! The Rust half of the same question. Two of Python's answers are not in
//! std at all, and saying so is the point rather than a gap in the port.

/// True for the combining marks in the five main blocks. `unicodedata.combining()`
/// reads the real property table; std has no such table, so this is the honest
/// approximation -- enough for the samples below, wrong in general.
fn is_combining(c: char) -> bool {
    matches!(c as u32,
        0x0300..=0x036F |   // Combining Diacritical Marks
        0x1AB0..=0x1AFF |   // ... Extended
        0x1DC0..=0x1DFF |   // ... Supplement
        0x20D0..=0x20FF |   // ... for Symbols
        0xFE20..=0xFE2F)    // Combining Half Marks
}

/// A crude grapheme count: a new cluster starts at any character that is not a
/// combining mark, not a ZWJ, and not preceded by a ZWJ. Real segmentation is
/// UAX #29; this is enough to show the gap exists.
fn clusters(text: &str) -> usize {
    let mut count = 0;
    let mut prev_zwj = false;
    for c in text.chars() {
        let zwj = c == '\u{200D}';
        if !is_combining(c) && !zwj && !prev_zwj {
            count += 1;
        }
        prev_zwj = zwj;
    }
    count
}

fn main() {
    let samples: [(&str, &str); 7] = [
        ("plain ASCII",     "cafe"),
        ("NFC - one char",  "caf\u{00E9}"),                       // é as U+00E9
        ("NFD - two chars", "cafe\u{0301}"),                      // e + COMBINING ACUTE
        ("Polish",          "Za\u{017C}\u{00F3}\u{0142}\u{0107}"),
        ("emoji",           "\u{1F600}"),
        ("flag",            "\u{1F1F5}\u{1F1F1}"),                // two regional indicators
        ("family",          "\u{1F468}\u{200D}\u{1F469}\u{200D}\u{1F467}"),
    ];

    println!("1. FOUR ANSWERS TO 'HOW LONG IS THIS?'");
    println!("     {:<18} {:>6} {:>6} {:>7} {:>10}", "sample", "chars", "utf-8", "utf-16", "graphemes");
    println!("     {:<18} {:>6} {:>6} {:>7} {:>10}", "", "points", "bytes", "units", "(human)");
    println!("     {}", "-".repeat(52));
    for (label, text) in samples {
        println!(
            "     {:<18} {:>6} {:>6} {:>7} {:>10}",
            label,
            text.chars().count(),      // code points -- Python's len()
            text.len(),                // BYTES -- Rust's len() is not Python's
            text.encode_utf16().count(),
            clusters(text),
        );
    }
    println!("\n     Read the 'family' row: one thing on your screen, five code points,");
    println!("     eighteen UTF-8 bytes. Every column is a legitimate answer to a");
    println!("     different question, and no single method answers more than one.");

    println!("\n2. WHERE RUST AND PYTHON PART COMPANY: len()");
    let word = "Za\u{017C}\u{00F3}\u{0142}\u{0107}";
    println!("     text                      {:?}", word);
    println!("     text.len()                {:>2}   <- BYTES. Python's len() says 6.", word.len());
    println!("     text.chars().count()      {:>2}   <- code points. This is Python's len().", word.chars().count());
    println!("\n     Same spelling, different question. Rust names the cheap answer");
    println!("     len() because it is O(1); counting chars is a walk. Python names");
    println!("     the useful answer len() and makes you ask for bytes. Neither is");
    println!("     hiding anything -- but code translated between them silently");
    println!("     changes meaning, and only for non-ASCII input.");

    println!("\n3. THE TRAP THAT LOOKS LIKE A BUG");
    let nfc = "caf\u{00E9}";
    let nfd = "cafe\u{0301}";
    println!("     nfc = {:?}   chars = {}", nfc, nfc.chars().count());
    println!("     nfd = {:?}   chars = {}", nfd, nfd.chars().count());
    println!("     they print identically:      {} == {}", nfc, nfd);
    println!("     nfc == nfd                   {}", nfc == nfd);
    println!("\n     Now the part std cannot do: there is no normalize() in Rust's");
    println!("     standard library. Python fixes this in one call; Rust needs the");
    println!("     unicode-normalization crate. std ships UTF-8 correctness, not");
    println!("     the Unicode character database -- casing and is_whitespace are");
    println!("     in, normalization and segmentation are out.");

    println!("\n4. WHAT wc COUNTS, AND WHICH METHOD MATCHES IT");
    let text = "Za\u{017C}\u{00F3}\u{0142}\u{0107} g\u{0119}\u{015B}l\u{0105} ja\u{017A}\u{0144}\n";
    println!("     text  = {:?}", text);
    println!("     bytes = {}   <- wc -c   text.len()", text.len());
    println!("     chars = {}   <- wc -m   text.chars().count()", text.chars().count());
    println!("     words = {}    <- wc -w   text.split_whitespace().count()", text.split_whitespace().count());
    println!("     lines = {}    <- wc -l   counts NEWLINES, not lines", text.matches('\n').count());
    println!("\n     wc -c and wc -m differ by 9 here, and a wc that only reads bytes");
    println!("     cannot tell you the second number at all.");

    println!("\n5. THE LINE COUNT IS A NEWLINE COUNT");
    for (label, sample) in [("with trailing \\n", "a\nb\n"), ("without", "a\nb")] {
        println!(
            "     {:<18} {:<10} matches('\\n') = {}   but there are {} lines",
            label, format!("{:?}", sample), sample.matches('\n').count(), sample.lines().count()
        );
    }
    println!("\n     Rust's .lines() is Python's .splitlines(): it answers the question");
    println!("     a person asked, while wc -l and a newline count answer a different");
    println!("     one. They agree only when the file ends in a newline.");

    println!("\n6. split_whitespace() IS NOT A WORD DEFINITION");
    for sample in ["one  two", "hyphen-ated", "don't", "\u{142}\u{F3}d\u{17A}\u{A0}\u{142}\u{F3}d\u{17A}"] {
        let words: Vec<&str> = sample.split_whitespace().collect();
        println!("     {:<26} -> {:>2} {:?}", format!("{:?}", sample), words.len(), words);
    }
    println!("\n     The last one holds a NO-BREAK SPACE (U+00A0). Rust's is_whitespace");
    println!("     uses the Unicode White_Space property, which includes it -- so Rust");
    println!("     and Python agree here, and both disagree with a tool that splits on");
    println!("     ASCII space alone. 'Word' is a policy, not a fact.");
}
