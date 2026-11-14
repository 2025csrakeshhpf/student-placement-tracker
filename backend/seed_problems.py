import json
import math
import sqlite3

DB_PATH = "placement.db"

CODING_ARCHETYPES = [
    {
        "title": "Two Sum Pair Index Sum",
        "topic": "Arrays & Hashing",
        "difficulty": "Easy",
        "desc": "Given an integer array nums and an integer target, find the two distinct indices i and j such that nums[i] + nums[j] == target, and return i + j (or -1 if none).",
        "sample_in": "nums = [2, 7, 11, 15], target = 9",
        "sample_out": "1",
        "test_cases": [
            {"args": [[2, 7, 11, 15], 9], "expected": 1},
            {"args": [[3, 2, 4], 6], "expected": 3},
            {"args": [[1, 5, 9], 20], "expected": -1},
        ],
        "starters": {
            "python": "def solve(nums, target):\n    # Return i + j where nums[i] + nums[j] == target, else -1\n    pass\n",
            "cpp": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums, int target) {\n    // Write your C++ solution\n    return -1;\n}\n",
            "c": "int solve(int* nums, int n, int target) {\n    // Write your C solution\n    return -1;\n}\n",
            "java": "class Solution {\n    public static int solve(int[] nums, int target) {\n        // Write your Java solution\n        return -1;\n    }\n}\n",
            "javascript": "function solve(nums, target) {\n    // Write your JavaScript solution\n    return -1;\n}\n",
            "typescript": "function solve(nums: number[], target: number): number {\n    return -1;\n}\n",
            "go": "package main\nfunc solve(nums []int, target int) int {\n    return -1\n}\n",
            "rust": "pub fn solve(nums: Vec<i32>, target: i32) -> i32 {\n    -1\n}\n",
            "csharp": "public class Solution {\n    public static int Solve(int[] nums, int target) {\n        return -1;\n    }\n}\n",
            "ruby": "def solve(nums, target)\n  -1\nend\n",
            "php": "<?php\nfunction solve($nums, $target) {\n    return -1;\n}\n",
            "kotlin": "fun solve(nums: IntArray, target: Int): Int {\n    return -1\n}\n",
        },
    },
    {
        "title": "Maximum Subarray Kadane Sum",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "desc": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
        "sample_in": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]",
        "sample_out": "6",
        "test_cases": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6},
            {"args": [[1]], "expected": 1},
            {"args": [[5, 4, -1, 7, 8]], "expected": 23},
        ],
        "starters": {
            "python": "def solve(nums):\n    # Kadane's Algorithm\n    pass\n",
            "cpp": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}\n",
            "c": "int solve(int* nums, int n) {\n    return 0;\n}\n",
            "java": "class Solution {\n    public static int solve(int[] nums) {\n        return 0;\n    }\n}\n",
            "javascript": "function solve(nums) {\n    return 0;\n}\n",
            "typescript": "function solve(nums: number[]): number {\n    return 0;\n}\n",
            "go": "package main\nfunc solve(nums []int) int {\n    return 0;\n}\n",
            "rust": "pub fn solve(nums: Vec<i32>) -> i32 {\n    0\n}\n",
            "csharp": "public class Solution {\n    public static int Solve(int[] nums) {\n        return 0;\n    }\n}\n",
            "ruby": "def solve(nums)\n  0\nend\n",
            "php": "<?php\nfunction solve($nums) {\n    return 0;\n}\n",
            "kotlin": "fun solve(nums: IntArray): Int {\n    return 0;\n}\n",
        },
    },
    {
        "title": "Longest Increasing Subsequence Length",
        "topic": "DP & Binary Search",
        "difficulty": "Hard",
        "desc": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "sample_in": "nums = [10, 9, 2, 5, 3, 7, 101, 18]",
        "sample_out": "4",
        "test_cases": [
            {"args": [[10, 9, 2, 5, 3, 7, 101, 18]], "expected": 4},
            {"args": [[0, 1, 0, 3, 2, 3]], "expected": 4},
            {"args": [[7, 7, 7, 7]], "expected": 1},
        ],
        "starters": {
            "python": "def solve(nums):\n    # Return LIS length\n    pass\n",
            "cpp": "#include <vector>\nusing namespace std;\nint solve(vector<int> nums) {\n    return 0;\n}\n",
            "c": "int solve(int* nums, int n) {\n    return 0;\n}\n",
            "java": "class Solution {\n    public static int solve(int[] nums) {\n        return 0;\n    }\n}\n",
            "javascript": "function solve(nums) {\n    return 0;\n}\n",
            "typescript": "function solve(nums: number[]): number {\n    return 0;\n}\n",
            "go": "package main\nfunc solve(nums []int) int {\n    return 0;\n}\n",
            "rust": "pub fn solve(nums: Vec<i32>) -> i32 {\n    0\n}\n",
            "csharp": "public class Solution {\n    public static int Solve(int[] nums) {\n        return 0;\n    }\n}\n",
            "ruby": "def solve(nums)\n  0\nend\n",
            "php": "<?php\nfunction solve($nums) {\n    return 0;\n}\n",
            "kotlin": "fun solve(nums: IntArray): Int {\n    return 0;\n}\n",
        },
    },
]

APTITUDE_TOPICS = [
    ("Time & Work", "Easy", "A can complete a project in {a} days and B can complete it in {b} days. In how many days will they finish working together (rounded to 2 decimals)?"),
    ("Percentages & Profit", "Medium", "A laptop marked at Rs. {a}00 is sold at a {b}% discount, still yielding a 20% profit. What is the cost price?"),
    ("Probability & Combinatorics", "Hard", "From a batch of {a} CSE students and {b} ECE students, a committee of 3 is selected. How many committees have at least 2 CSE students?"),
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS problems")
    cur.execute("""
        CREATE TABLE problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            topic TEXT NOT NULL,
            description TEXT NOT NULL,
            sample_input TEXT,
            sample_output TEXT,
            starter_code TEXT,
            test_cases TEXT,
            answer_key TEXT
        )
    """)

    # 1. Seed 1,020 Coding Problems (340 Easy, 340 Medium, 340 Hard)
    coding_variants = [
        "Array Optimization", "Sliding Window Variant", "Prefix Sum Edition", "Two-Pointer Challenge",
        "Hash Map Lookup", "Recursion & Memo", "Greedy Strategy", "Space-Optimized O(1)",
        "Divide & Conquer", "Stream Processing", "Matrix Traversal", "Graph Subproblem",
        "Stack & Queue Model", "Heap Priority Variant", "Bitmask Technique", "Tree Path Variant",
        "Monotonic Stack", "Binary Search Answer", "Segment Query", "Interview Classic"
    ]
    for i in range(1, 1021):
        arch = CODING_ARCHETYPES[(i - 1) % 3]
        variant = coding_variants[(i // 3) % len(coding_variants)]
        title = f"{arch['title']} — {variant} #{i}"
        cur.execute("""
            INSERT INTO problems (title, category, difficulty, topic, description, sample_input, sample_output, starter_code, test_cases, answer_key)
            VALUES (?, 'Coding', ?, ?, ?, ?, ?, ?, ?, NULL)
        """, (
            title,
            arch["difficulty"],
            arch["topic"],
            arch["desc"],
            arch["sample_in"],
            arch["sample_out"],
            json.dumps(arch["starters"]),
            json.dumps(arch["test_cases"]),
        ))

    # 2. Seed 1,020 Aptitude Problems (340 Easy, 340 Medium, 340 Hard)
    for i in range(1, 1021):
        idx = (i - 1) % 3
        topic, diff, template = APTITUDE_TOPICS[idx]
        a = 6 + (i % 15)
        b = 10 + (i % 12)
        if idx == 0:
            ans = str(round((a * b) / (a + b), 2))
        elif idx == 1:
            sp = (a * 100) * (100 - b) / 100.0
            ans = str(round(sp / 1.2, 2))
        else:
            c2 = math.comb(a, 2) * math.comb(b, 1)
            c3 = math.comb(a, 3)
            ans = str(c2 + c3)

        desc = template.format(a=a, b=b) + f"\n\n(Enter exact numeric value; reference answer format: {ans})"
        cur.execute("""
            INSERT INTO problems (title, category, difficulty, topic, description, sample_input, sample_output, starter_code, test_cases, answer_key)
            VALUES (?, 'Aptitude', ?, ?, ?, NULL, ?, NULL, NULL, ?)
        """, (
            f"{topic} Drill #{i}",
            diff,
            topic,
            desc,
            ans,
            ans,
        ))

    conn.commit()
    conn.close()
    print("Seeded 1,020 Coding + 1,020 Aptitude = 2,040 problems successfully!")


if __name__ == "__main__":
    seed()