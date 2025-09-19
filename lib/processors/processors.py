class TextProcessor:
    def process(self, text: list[str]) -> list[str]:
        return [line.strip() + "1" for line in text]
