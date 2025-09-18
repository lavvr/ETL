class TextProcessor:
    def process(self, text):
        return [line.strip() + "1" for line in text]
