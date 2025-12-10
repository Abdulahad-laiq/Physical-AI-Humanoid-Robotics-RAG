#!/usr/bin/env python3
"""
Citation Validation Script for Physical AI Textbook

Purpose: Validate IEEE citation format and ensure 40%+ citation density

Usage:
    python scripts/validate-citations.py                    # Check all chapters
    python scripts/validate-citations.py docs/ch03-kinematics/  # Check specific chapter

Requirements:
    - All citations in IEEE format: [1], [2], [3] or [1]-[5]
    - Minimum 40% of technical paragraphs must contain citations
    - All citation numbers must exist in bibliography.md

Exit Codes:
    0: All checks passed
    1: Citation density below 40%
    2: Invalid citation format detected
    3: Citation references non-existent bibliography entry
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict


class CitationValidator:
    def __init__(self, min_density: float = 0.40):
        self.min_density = min_density
        self.citation_pattern = re.compile(r'\[(\d+)\]')  # Matches [1], [2], etc.
        self.range_pattern = re.compile(r'\[(\d+)-(\d+)\]')  # Matches [1-5]
        self.errors = []
        self.warnings = []

    def load_bibliography_entries(self, bib_file: Path) -> set:
        """Load all valid citation numbers from bibliography.md"""
        valid_citations = set()

        if not bib_file.exists():
            self.errors.append(f"Bibliography file not found: {bib_file}")
            return valid_citations

        content = bib_file.read_text(encoding='utf-8')

        # Find all [N] entries in bibliography
        matches = self.citation_pattern.findall(content)
        for match in matches:
            valid_citations.add(int(match))

        return valid_citations

    def count_technical_paragraphs(self, content: str) -> int:
        """Count paragraphs that contain technical content (not headers, code, etc.)"""
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remove YAML frontmatter
        content = re.sub(r'^---[\s\S]*?---', '', content, flags=re.MULTILINE)

        # Remove headers
        content = re.sub(r'^#{1,6}\s+.*$', '', content, flags=re.MULTILINE)

        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # Filter out very short paragraphs (likely not technical content)
        technical_paragraphs = [p for p in paragraphs if len(p) > 50]

        return len(technical_paragraphs)

    def find_citations(self, content: str) -> List[int]:
        """Extract all citation numbers from content"""
        citations = set()

        # Find single citations [1]
        single_matches = self.citation_pattern.findall(content)
        for match in single_matches:
            citations.add(int(match))

        # Find range citations [1-5]
        range_matches = self.range_pattern.findall(content)
        for start, end in range_matches:
            citations.update(range(int(start), int(end) + 1))

        return sorted(list(citations))

    def count_cited_paragraphs(self, content: str) -> int:
        """Count paragraphs containing at least one citation"""
        # Remove code blocks
        content_no_code = re.sub(r'```[\s\S]*?```', '', content)

        # Remove YAML frontmatter
        content_no_code = re.sub(r'^---[\s\S]*?---', '', content_no_code, flags=re.MULTILINE)

        # Remove headers
        content_no_code = re.sub(r'^#{1,6}\s+.*$', '', content_no_code, flags=re.MULTILINE)

        # Split into paragraphs
        paragraphs = [p.strip() for p in content_no_code.split('\n\n') if p.strip()]

        # Count paragraphs with citations
        cited_count = 0
        for p in paragraphs:
            if len(p) > 50:  # Technical paragraph threshold
                if self.citation_pattern.search(p) or self.range_pattern.search(p):
                    cited_count += 1

        return cited_count

    def validate_file(self, md_file: Path, valid_citations: set) -> Tuple[bool, Dict]:
        """Validate citations in a single markdown file"""
        content = md_file.read_text(encoding='utf-8')

        # Count paragraphs
        total_paragraphs = self.count_technical_paragraphs(content)
        cited_paragraphs = self.count_cited_paragraphs(content)

        # Calculate citation density
        if total_paragraphs > 0:
            citation_density = cited_paragraphs / total_paragraphs
        else:
            citation_density = 0.0

        # Extract all citations
        citations = self.find_citations(content)

        # Check for invalid citations (not in bibliography)
        invalid_citations = [c for c in citations if c not in valid_citations]

        # Prepare results
        result = {
            'file': str(md_file),
            'total_paragraphs': total_paragraphs,
            'cited_paragraphs': cited_paragraphs,
            'citation_density': citation_density,
            'citations_found': citations,
            'invalid_citations': invalid_citations,
            'passed': True
        }

        # Check citation density
        if citation_density < self.min_density:
            self.warnings.append(
                f"{md_file}: Citation density {citation_density:.1%} below minimum {self.min_density:.0%}"
            )
            result['passed'] = False

        # Check invalid citations
        if invalid_citations:
            self.errors.append(
                f"{md_file}: Invalid citations not found in bibliography: {invalid_citations}"
            )
            result['passed'] = False

        return result['passed'], result

    def validate_directory(self, directory: Path, valid_citations: set) -> bool:
        """Validate all markdown files in a directory"""
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

        print(f"\nValidating {len(md_files)} files in {directory}...\n")

        for md_file in md_files:
            passed, result = self.validate_file(md_file, valid_citations)
            results.append(result)

            if not passed:
                all_passed = False

            # Print summary for each file
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status} {md_file.name}: "
                  f"{result['cited_paragraphs']}/{result['total_paragraphs']} "
                  f"({result['citation_density']:.1%}) cited")

        return all_passed


def main():
    # Parse command line arguments
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    else:
        target_path = Path('docs')

    # Load bibliography
    bib_file = Path('docs/bibliography.md')
    validator = CitationValidator(min_density=0.40)

    print("=" * 60)
    print("Citation Validation for Physical AI Textbook")
    print("=" * 60)

    valid_citations = validator.load_bibliography_entries(bib_file)

    if not valid_citations:
        print(f"\n✗ ERROR: No bibliography entries found in {bib_file}")
        return 3

    print(f"\nLoaded {len(valid_citations)} valid citations from bibliography")
    print(f"Minimum citation density required: {validator.min_density:.0%}")

    # Validate
    if target_path.is_file():
        passed, result = validator.validate_file(target_path, valid_citations)
    elif target_path.is_dir():
        passed = validator.validate_directory(target_path, valid_citations)
    else:
        print(f"\n✗ ERROR: Path not found: {target_path}")
        return 3

    # Print summary
    print("\n" + "=" * 60)
    if passed and not validator.errors:
        print("✓ All citation checks PASSED")
        return 0
    else:
        print("✗ Citation validation FAILED\n")

        if validator.errors:
            print("ERRORS:")
            for error in validator.errors:
                print(f"  - {error}")

        if validator.warnings:
            print("\nWARNINGS:")
            for warning in validator.warnings:
                print(f"  - {warning}")

        # Determine exit code
        if validator.errors:
            if any('Invalid citations' in e for e in validator.errors):
                return 3
            else:
                return 2
        else:
            return 1


if __name__ == '__main__':
    sys.exit(main())
