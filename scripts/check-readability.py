#!/usr/bin/env python3
"""
Readability Analysis Script for Physical AI Textbook

Purpose: Validate Flesch-Kincaid grade level is between 10-14

Usage:
    python scripts/check-readability.py                    # Check all chapters
    python scripts/check-readability.py docs/ch03-kinematics/  # Check specific chapter

Requirements:
    - Flesch-Kincaid Grade Level: 10-14 (university-level accessible)
    - Flesch Reading Ease: 40-60 (college-level)

Exit Codes:
    0: All checks passed
    1: Readability outside target range
"""

import re
import sys
from pathlib import Path
from typing import Dict, Tuple
import textstat


class ReadabilityChecker:
    def __init__(self, min_grade: float = 10.0, max_grade: float = 14.0):
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.errors = []
        self.warnings = []

    def extract_text_content(self, content: str) -> str:
        """Extract readable text, removing code blocks, YAML, etc."""
        # Remove YAML frontmatter
        content = re.sub(r'^---[\s\S]*?---', '', content, flags=re.MULTILINE)

        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)

        # Remove citations [1], [2], etc.
        content = re.sub(r'\[\d+\]', '', content)
        content = re.sub(r'\[\d+-\d+\]', '', content)

        # Remove Markdown headers (but keep the text)
        content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

        # Remove Markdown links but keep text: [text](url) -> text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # Remove Markdown bold/italic markers
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)

        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)

        # Remove LaTeX math (both inline and block)
        content = re.sub(r'\$\$[\s\S]*?\$\$', '', content)
        content = re.sub(r'\$[^\$]+\$', '', content)

        # Remove excess whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()

        return content

    def analyze_file(self, md_file: Path) -> Tuple[bool, Dict]:
        """Analyze readability of a single markdown file"""
        content = md_file.read_text(encoding='utf-8')
        text = self.extract_text_content(content)

        # Skip files with too little content
        if len(text) < 100:
            return True, {
                'file': str(md_file),
                'word_count': 0,
                'fk_grade': None,
                'flesch_ease': None,
                'passed': True,
                'skipped': True
            }

        # Calculate readability metrics
        try:
            fk_grade = textstat.flesch_kincaid_grade(text)
            flesch_ease = textstat.flesch_reading_ease(text)
            word_count = textstat.lexicon_count(text, removepunct=True)
        except Exception as e:
            self.errors.append(f"{md_file}: Error calculating readability: {e}")
            return False, {
                'file': str(md_file),
                'error': str(e),
                'passed': False
            }

        # Check if grade level is in acceptable range
        passed = self.min_grade <= fk_grade <= self.max_grade

        if not passed:
            if fk_grade < self.min_grade:
                self.warnings.append(
                    f"{md_file}: FK grade {fk_grade:.1f} below minimum {self.min_grade} "
                    f"(may be too simple)"
                )
            else:
                self.errors.append(
                    f"{md_file}: FK grade {fk_grade:.1f} above maximum {self.max_grade} "
                    f"(too complex for target audience)"
                )

        result = {
            'file': str(md_file),
            'word_count': word_count,
            'fk_grade': fk_grade,
            'flesch_ease': flesch_ease,
            'passed': passed,
            'skipped': False
        }

        return passed, result

    def analyze_directory(self, directory: Path) -> bool:
        """Analyze all markdown files in a directory"""
        all_passed = True
        results = []

        # Find all markdown files
        md_files = list(directory.rglob('*.md'))

        # Skip certain files
        skip_files = {'intro.md', 'glossary.md', 'bibliography.md', 'README.md'}
        md_files = [f for f in md_files if f.name not in skip_files]

        if not md_files:
            print(f"No markdown files found in {directory}")
            return True

        print(f"\nAnalyzing {len(md_files)} files in {directory}...\n")

        for md_file in md_files:
            passed, result = self.analyze_file(md_file)
            results.append(result)

            if not result.get('skipped', False):
                if not passed:
                    all_passed = False

                # Print summary for each file
                status = "✓ PASS" if passed else "✗ FAIL"
                fk_grade = result.get('fk_grade', 0)
                word_count = result.get('word_count', 0)
                print(f"{status} {md_file.name}: FK grade {fk_grade:.1f}, "
                      f"{word_count} words")

        # Print aggregate statistics
        if results:
            valid_results = [r for r in results if not r.get('skipped', False)]
            if valid_results:
                avg_grade = sum(r['fk_grade'] for r in valid_results) / len(valid_results)
                avg_ease = sum(r['flesch_ease'] for r in valid_results) / len(valid_results)

                print("\n" + "-" * 60)
                print(f"Average FK Grade Level: {avg_grade:.1f} "
                      f"(target: {self.min_grade}-{self.max_grade})")
                print(f"Average Reading Ease: {avg_ease:.1f} (40-60 = college level)")

        return all_passed


def main():
    # Parse command line arguments
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    else:
        target_path = Path('docs')

    checker = ReadabilityChecker(min_grade=10.0, max_grade=14.0)

    print("=" * 60)
    print("Readability Analysis for Physical AI Textbook")
    print("=" * 60)
    print(f"Target Flesch-Kincaid Grade Level: {checker.min_grade}-{checker.max_grade}")
    print(f"Target Audience: University students (ages 17-25)")

    # Validate
    if target_path.is_file():
        passed, result = checker.analyze_file(target_path)
        if not result.get('skipped', False):
            print(f"\nFile: {target_path.name}")
            print(f"  FK Grade Level: {result['fk_grade']:.1f}")
            print(f"  Flesch Reading Ease: {result['flesch_ease']:.1f}")
            print(f"  Word Count: {result['word_count']}")
    elif target_path.is_dir():
        passed = checker.analyze_directory(target_path)
    else:
        print(f"\n✗ ERROR: Path not found: {target_path}")
        return 1

    # Print summary
    print("\n" + "=" * 60)
    if passed and not checker.errors:
        print("✓ All readability checks PASSED")
        return 0
    else:
        print("✗ Readability validation FAILED\n")

        if checker.errors:
            print("ERRORS (content too complex):")
            for error in checker.errors:
                print(f"  - {error}")

        if checker.warnings:
            print("\nWARNINGS (content may be too simple):")
            for warning in checker.warnings:
                print(f"  - {warning}")

        return 1


if __name__ == '__main__':
    sys.exit(main())
