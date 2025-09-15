class TextProcessor:
    def process(self, text):
        return [line.strip() + '\n' for line in text]
