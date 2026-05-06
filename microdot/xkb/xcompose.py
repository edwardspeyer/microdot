from pathlib import Path
from typing import Iterable, Iterator, TypeAlias
from unicodedata import name

Greek = """
a α  b β  g γ  d δ  e ε  z ζ  h η  j θ  i ι  k κ  l λ  m μ
A Α  B Β  G Γ  D Δ  E Ε  Z Ζ  H Η  J Θ  I Ι  K Κ  L Λ  M Μ
n ν  x ξ  o ο  p π  r ρ  s σ  t τ  u υ  f φ  q χ  y ψ  w ω
N Ν  X Ξ  O Ο  P Π  R Ρ  S Σ  T Τ  U Υ  F Φ  Q Χ  Y Ψ  W Ω
"""

Fraktur = """
a 𝔞  b 𝔟  c 𝔠  d 𝔡  e 𝔢  f 𝔣  g 𝔤  h 𝔥  i 𝔦  j 𝔧  k 𝔨  l 𝔩  m 𝔪
A 𝔄  B 𝔅  C ℭ  D 𝔇  E 𝔈  F 𝔉  G 𝔊  H ℌ  I ℑ  J 𝔍  K 𝔎  L 𝔏  M 𝔐
n 𝔫  o 𝔬  p 𝔭  q 𝔮  r 𝔯  s 𝔰  t 𝔱  u 𝔲  v 𝔳  w 𝔴  x 𝔵  y 𝔶  z 𝔷
N 𝔑  O 𝔒  P 𝔓  Q 𝔔  R ℜ  S 𝔖  T 𝔗  U 𝔘  V 𝔙  W 𝔚  X 𝔛  Y 𝔜  Z ℨ
"""

Blackboard = """
a 𝕒  b 𝕓  c 𝕔  d 𝕕  e 𝕖  f 𝕗  g 𝕘  h 𝕙  i 𝕚  j 𝕛  k 𝕜  l 𝕝  m 𝕞
A 𝔸  B 𝔹  C ℂ  D 𝔻  E 𝔼  F 𝔽  G 𝔾  H ℍ  I 𝕀  J 𝕁  K 𝕂  L 𝕃  M 𝕄
n 𝕟  o 𝕠  p 𝕡  q 𝕢  r 𝕣  s 𝕤  t 𝕥  u 𝕦  v 𝕧  w 𝕨  x 𝕩  y 𝕪  z 𝕫
N ℕ  O 𝕆  P ℙ  Q ℚ  R ℝ  S 𝕊  T 𝕋  U 𝕌  V 𝕍  W 𝕎  X 𝕏  Y 𝕐  Z ℤ
"""

Node: TypeAlias = tuple[str, str | Iterable["Node"]]

Config: list[Node] = [
    (
        "Multi_key",
        [
            ("3", "£"),
            ("-", "–"),
            ("'", [("e", "é")]),
            ("g", Greek),
            ("d", Fraktur),
            ("b", Blackboard),
        ],
    )
]

# The names of chars sent by our keyboard, from /usr/include/X11/keysymdef.h:
KEYSYMS = {
    " ": "space",
    "!": "exclam",
    '"': "quotedbl",
    "#": "numbersign",
    "$": "dollar",
    "%": "percent",
    "&": "ampersand",
    "'": "quoteright",
    "(": "parenleft",
    ")": "parenright",
    "*": "asterisk",
    "+": "plus",
    ",": "comma",
    "-": "minus",
    ".": "period",
    "/": "slash",
    ":": "colon",
    ";": "semicolon",
    "<": "less",
    "=": "equal",
    ">": "greater",
    "?": "question",
    "@": "at",
    "[": "bracketleft",
    "\\": "backslash",
    "]": "bracketright",
    "^": "asciicircum",
    "_": "underscore",
    "`": "quoteleft",
    "{": "braceleft",
    "|": "bar",
    "}": "braceright",
    "~": "asciitilde",
}


def tabulate(rows: Iterable[Iterable[str]]) -> str:
    widths = [max(len(c) for c in col) for col in zip(*rows)]
    return "".join(" ".join(c.ljust(w) for c, w in zip(row, widths)).rstrip() + "\n" for row in rows)


def pairs(cs: list[str]) -> list[tuple[str, str]]:
    assert len(cs) % 2 == 0
    return [(cs[i + 0], cs[i + 1]) for i in range(0, len(cs), 2)]


def compile(nodes: Iterable[Node]) -> str:
    seen = set()

    def walk(keys: list[str], v: str | Iterable[Node]) -> Iterator[list[str]]:
        # (1) Convert multi-line strings into nodes
        if isinstance(v, str) and len(v) > 1:
            v = pairs(v.strip().split())

        # (2) Terminate or recurse down the tree
        if isinstance(v, str):
            prefix = " ".join(f"<{KEYSYMS.get(k, k)}>" for k in keys)
            assert prefix not in seen, f"Already seen! {prefix!r}"
            yield [prefix, ":", f'"{v}"', " #", name(v)]
            seen.add(prefix)
        else:
            for k, child in v:  # type: ignore[misc] # ... we know it's not a str
                yield from walk([*keys, k], child)

    return tabulate(list(walk([], nodes)))


def build_xcompose() -> Path:
    path = Path.home() / ".cache" / "microdot" / "XCompose"
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(compile(Config))
    return path
