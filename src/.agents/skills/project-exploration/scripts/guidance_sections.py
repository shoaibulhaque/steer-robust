"""Small ATX/fence parser that retains children and ancestor introductions."""
import re


def headings(lines):
    marks, fence = [], None
    for index, line in enumerate(lines):
        token = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if token:
            marker = token.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[token.end():].strip():
                fence = None
            continue
        match = None if fence else re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if match:
            marks.append((index, len(match[1]), match[2]))
    return marks


def selections(lines, heading=None, match=None):
    marks = headings(lines)
    if not marks or marks[0][0] > 0:
        marks.insert(0, (0, 0, "[preamble]"))
    stack, selected, covered = [], [], -1
    for i, (start, level, title) in enumerate(marks):
        own_end = marks[i + 1][0] if i + 1 < len(marks) else len(lines)
        end = next((s for s, depth, _ in marks[i + 1:] if depth <= level), len(lines)) if level else own_end
        while stack and stack[-1][2] >= level:
            stack.pop()
        lead = "\n".join(lines[start:own_end])
        accepted = (heading is None or heading.search(title)) and (match is None or match.search(lead))
        if accepted and start >= covered:
            ranges = [(s, e) for s, e, _ in stack] + [(start, end)]
            # Keep shared lead-ins separate so the caller can emit them once without losing scope.
            selected.append((title, ranges))
            covered = end
        stack.append((start, own_end, level))
    return selected
