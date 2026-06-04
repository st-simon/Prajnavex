import argparse

from knowledge_index import build_index, scalar


def iter_bundles(records):
    for record in records:
        if scalar(record.get("type")) == "bundle":
            yield record


def render_draft(bundle):
    title = scalar(bundle.get("title"))
    bundle_id = scalar(bundle.get("id"))
    inputs = scalar(bundle.get("input_contract")) or "Describe required inputs."
    outputs = scalar(bundle.get("output_contract")) or "Describe expected outputs."
    return "\n".join([
        f"# Tool Draft: {title}",
        "",
        f"Bundle: `{bundle_id}`",
        "",
        "## Inputs",
        inputs,
        "",
        "## Outputs",
        outputs,
        "",
        "## Workflow",
        "Convert the bundle skills into executable steps before use.",
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="list available bundles")
    parser.add_argument("--bundle-id", help="render one bundle as a workflow draft")
    args = parser.parse_args()
    records, errors, _ = build_index()
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    bundles = list(iter_bundles(records))
    if args.list:
        for bundle in bundles:
            print(f"{scalar(bundle.get('id'))}\t{scalar(bundle.get('title'))}")
        return
    if args.bundle_id:
        for bundle in bundles:
            if scalar(bundle.get("id")) == args.bundle_id:
                print(render_draft(bundle))
                return
        raise SystemExit(f"bundle not found: {args.bundle_id}")
    parser.print_help()


if __name__ == "__main__":
    main()
