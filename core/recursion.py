from core.domain import Resume


def walk_skills_tree(tree: dict, skill: str) -> tuple[str, ...]:
    result = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == skill:
                    result.append(k)
                    result.extend(walk(v))
                else:
                    result.extend(walk(v))
        elif isinstance(node, list):
            for item in node:
                result.extend(walk(item))
        return result

    return tuple(set(walk(tree)))


def expand_resume_fields(r: Resume, keys: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(r.parsed.get(k, "") for k in keys)
