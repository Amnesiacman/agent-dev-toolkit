import argparse
from pathlib import Path
from .env_tools import init_env, doctor_env

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
    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "env" and args.env_command == "init":
        ok, msg = init_env(Path(args.template), Path(args.output), args.force)
        print(msg)
        return 0 if ok else 1

    if args.command == "env" and args.env_command == "doctor":
        ok, msg = doctor_env(Path(args.template), Path(args.env_file))
        print(msg)
        return 0 if ok else 1

    parser.print_help()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
