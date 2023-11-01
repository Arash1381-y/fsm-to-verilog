import argparse
from verilog_transformer import VerilogTransformer


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to Verilog")
    parser.add_argument("json_path", help="Path to the JSON file")
    parser.add_argument("--result_path", help="Path to save the generated Verilog (optional)")

    args = parser.parse_args()

    vt = VerilogTransformer(args.json_path, args.result_path)
    vt.run()


if __name__ == "__main__":
    main()
