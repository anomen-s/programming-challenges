use std::fs::File;
use std::io::{BufRead, BufReader, Result};
use std::collections::HashMap;
use regex::Regex;
use lazy_static::lazy_static;

fn read_file_to_list(file_path: &str) -> Result<Vec<String>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);

    let mut lines = Vec::new();

    for line in reader.lines() {
        lines.push(line?);
    }

    Ok(lines)
}

lazy_static! {
    static ref NUM_REGEX: Regex = Regex::new(r"one|two|three|four|five|six|seven|eight|nine|\d").unwrap();

    static ref NUMBER_MAP: HashMap<String, i32> = {
        let mut map = HashMap::new();
        let nums1 = vec!["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
        for (index, value) in nums1.iter().enumerate() {
            let i : i32 = index as i32;
            map.insert(value.to_string(), i);
            map.insert(i.to_string(), i);
        }
        map
    };
}

fn find_first_digit(iter: impl Iterator<Item = char>) -> Option<i32> {
    for c in iter {
        if c.is_digit(10) {
            if let Some(digit) = c.to_digit(10) {
                return Some(digit as i32);
            }
        }
    }
    None
}

fn compute_line_value_part1(line: &str) -> i32 {
        let first = find_first_digit(line.chars());
        let last = find_first_digit(line.chars().rev());
        match (first, last) {
            (Some(n1), Some(n2)) => Some(n1 * 10 + n2),
            _ => None
        }.unwrap()
}

fn get_number(number: &str) -> i32 {
    *NUMBER_MAP.get(number).unwrap()
}

fn find_first_number(line: &str) -> i32 {

    get_number(NUM_REGEX.find(line).unwrap().as_str())
}

fn find_last_number(line: &str) -> i32 {
    let mut last_num = 0;
    for (index, _) in line.char_indices() {
        if let Some(m) = NUM_REGEX.find_at(&line, index) {
            let number = get_number(m.as_str());
            last_num = number;
        }
    }
    last_num
}

fn compute_line_value_part2(line: &str) -> i32 {

    find_first_number(line) * 10 + find_last_number(line)
}

fn solve_part1(file_name: &str) {
    if let Ok(lines) = read_file_to_list(file_name) {
        let sum : i32 = lines
                .into_iter()
                .map(|s| compute_line_value_part1(&s))
                .sum();
        println!("sum: {sum}");
    }
}

fn solve_part2(file_name: &str) {
    if let Ok(lines) = read_file_to_list(file_name) {
        let sum : i32 = lines
                .into_iter()
                .map(|s| compute_line_value_part2(&s))
                .sum();
        println!("sum: {sum}");
    }
}

fn main() {
    println!("Part 1 (142, 54561)");
    solve_part1("input.sample1");
    solve_part1("input");
    println!("Part 2 (281, 54076)");
    solve_part2("input.sample2");
    solve_part2("input");

}

