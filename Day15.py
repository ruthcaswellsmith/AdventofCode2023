from utils import read_file


class Lens:
    def __init__(self, text: str):
        self.text = text
        self.operation = "-" if "-" in self.text else "="
        pts = self.text.split(self.operation)
        self.label = pts[0]
        self.focal_length = int(pts[1]) if self.operation == '=' else None
        self.box = self.hash_val(self.label)
        self.slot = None
        self.next = None

    def hash_val(self, text: str) -> int:
        val = 0
        for char in text:
            val += ord(char)
            val *= 17
            val &= 255
        return val


class Box:
    def __init__(self):
        self.head = None

    def append(self, lens: Lens):
        if not self.head:
            self.head = lens
            lens.slot = 1
        else:
            ind = 2
            current = self.head
            while current.next:
                current = current.next
                ind += 1
            current.next = lens
            lens.slot = ind

    def display(self):
        current = self.head
        while current:
            print(f"{current.label}-{current.focal_length}", end=" -> ")
            current = current.next
        print("None")

    def find(self, label: str):
        current = self.head
        while current:
            if current.label == label:
                return current
            current = current.next
        return None

    def remove(self, label: str):
        current = self.head
        previous = None

        renumber = False
        while current:
            if current.label == label:
                renumber = True
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
            if renumber:
                current.slot -= 1

            previous = current
            current = current.next

    def replace(self, lens: Lens):
        node_to_replace = self.find(lens.label)
        if node_to_replace:
            node_to_replace.focal_length = lens.focal_length

    @property
    def focusing_powers(self):
        focusing_powers = {}
        current = self.head
        while current:
            focusing_powers[current.label] = current.slot * current.focal_length
            current = current.next

        return focusing_powers


if __name__ == '__main__':
    filename = 'input/Day15.txt'
    data = read_file(filename)

    lenses = [Lens(s) for s in data[0].split(',')]
    print(f"The answer to part 1 is {sum([lens.hash_val(lens.text) for lens in lenses])}.")

    boxes = {i: Box() for i in range(max([lens.box for lens in lenses]) + 1)}
    for i, lens in enumerate(lenses):
        box_num = lens.hash_val(lens.label)
        contents = boxes.get(box_num)
        if lens.operation == '-':
            if contents.head:
                contents.remove(lens.label)
        else:
            if contents.find(lens.label):
                contents.replace(lens)
            else:
                contents.append(lens)

    print(f"The answer to part 2 is "
          f"{sum([(box_num + 1) * sum(val.focusing_powers.values()) for box_num, val in boxes.items()])}.")
