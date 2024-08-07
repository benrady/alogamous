from alogamous import analyzer, log_line_parser


class StartupHeaderAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.line_parser = line_parser
        self.startup_block = False
        self.startup_lines = []

    def read_log_line(self, line):
        line_type = self.line_parser.parse(line)["type"]
        if self.startup_block is False and line_type == log_line_parser.LineType.HEADER_LINE:
            self.startup_block = True
        elif self.startup_block is True:
            if line_type == log_line_parser.LineType.UNSTRUCTURED_LINE:
                self.startup_lines.append(line)
            elif line_type == log_line_parser.LineType.HEADER_LINE:
                self.startup_block = False

    def report(self, out_stream):
        out_stream.write("Lines that are part of the startup header(s):\n- ")
        out_stream.write("\n- ".join(self.startup_lines))
