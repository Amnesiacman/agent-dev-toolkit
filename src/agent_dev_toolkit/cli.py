import argparse
import json
from pathlib import Path
from typing import Optional
from .env_tools import init_env, doctor_env, doctor_env_report


def _emit_output(text: str, output_path: Optional[str]):
    if output_path:
        Path(output_path).write_text(text + "\n", encoding="utf-8")
    print(text)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="agent-toolkit",
        description="Automation-friendly CLI for everyday development workflows.",
    )
    sub = parser.add_subparsers(dest="command")

    env = sub.add_parser("env", help="Environment file utilities")
    env_sub = env.add_subparsers(dest="env_command")

    p_init = env_sub.add_parser("init", help="Create .env from template")
    p_init.add_argument("--template", default=".env.example")
    p_init.add_argument("--output", default=".env")
    p_init.add_argument("--force", action="store_true")

    p_doc = env_sub.add_parser("doctor", help="Validate .env keys")
    p_doc.add_argument("--template", default=".env.example")
    p_doc.add_argument("--env-file", default=".env")
    p_doc.add_argument(
        "--allow-extra",
        action="store_true",
        help="Ignore extra keys in .env that are not in template",
    )
    p_doc.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any difference including extra keys",
    )
    p_doc.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for doctor command",
    )
    p_doc.add_argument(
        "--output",
        help="Write command output to file path",
    )
    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "env" and args.env_command == "init":
        ok, msg = init_env(Path(args.template), Path(args.output), args.force)
        print(msg)
        return 0 if ok else 1

    if args.command == "env" and args.env_command == "doctor":
        template_path = Path(args.template)
        env_path = Path(args.env_file)
        if args.format == "json":
            report = doctor_env_report(
                template_path,
                env_path,
                allow_extra=args.allow_extra,
                strict=args.strict,
            )
            _emit_output(
                json.dumps(report, ensure_ascii=True),
                args.output,
            )
            return 0 if report["ok"] else 1
        ok, msg = doctor_env(
            template_path,
            env_path,
            allow_extra=args.allow_extra,
            strict=args.strict,
        )
        _emit_output(msg, args.output)
        return 0 if ok else 1

    parser.print_help()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
