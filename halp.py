import codecs
import io
import pydoc
import tokenize


# thanks to Python-wizard Akuli for showing me how to abuse codecs :)
# see his self-harming tutorial https://github.com/Akuli/import-that
# if you like this


class HelpEncodingIterator:

    def __init__(self, tokens):
        self.iterator = (
            token
            for token in tokens
            if token.type not in (tokenize.NEWLINE, tokenize.COMMENT)
        )
        self._coming_up = None

    @property
    def coming_up(self):
        if self._coming_up is None:
            try:
                self._coming_up = next(self.iterator)
            except StopIteration:
                return None
        return self._coming_up

    def __iter__(self):
        return self

    def __next__(self):
        if self._coming_up is None:
            return next(self.iterator)
        tmp = self._coming_up
        self._coming_up = None
        return tmp

    def __bool__(self):
        return self.coming_up is not None


class HelpEncoding:

    def __init__(self, tokens):
        self.tokens = HelpEncodingIterator(tokens)
        self.output = []

    def parse(self):
        while self.tokens:
            self._parse_token()

    def _parse_token(self):
        token = next(self.tokens)
        self.output.append(token)
        if not (token.type == tokenize.NAME and token.string == "help"):
            return

        paren = next(self.tokens)
        self.output.append(paren)
        if paren.string != "(":
            return

        inner = next(self.tokens)
        if inner.string in pydoc.Helper.keywords:
            self.output.append(
                tokenize.TokenInfo(
                    type=tokenize.STRING,
                    string=repr(inner.string),
                    start=inner.start,
                    end=inner.end,
                    line=inner.line,
                )
            )
        else:
            self.output.append(inner)


def encode(string, errors="strict"):
    raise NotImplemented("this is nonsense, right?")


def decode(byteslike, errors="strict"):
    code_bytes = bytes(byteslike)
    decoder = HelpEncoding(
        tokenize.tokenize(io.BytesIO(b"(" + code_bytes + b")").readline)
    )
    decoder.parse()
    return (tokenize.untokenize(decoder.output[2:-2]), len(code_bytes))


codec_info = codecs.CodecInfo(encode, decode, name="halp")
codecs.register({"halp": codec_info}.get)
