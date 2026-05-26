class Urlshorter:
    def __init__(self):
        self.table = HashTable()
        self.generator = CodeGenerator() # Выдавать короткий код +

    def add_url(self, url: str): #Добавление новой ссылки +
        short_url = self.generator.next_code()

        while self.table.contains(short_url): #Запрет создания двух одинаковых кодов +
            short_url = self.generator.next_code()

        self.table.put(short_url, url) #Сохраняет длинную ссылку + => Получение длинной сслыки по короткому коду +
        return short_url

    def get_url(self, short_url: str):
        return self.table.get(short_url)

    def exists(self, short_url: str): # Проверка существования короткого кода +
        return self.table.contains(short_url)

    def list_all(self): # Вывод всех сокращённых ссылок +
        return self.table.items()


class HashTable:
    def __init__(self, cap=101, load_proc = 0.5):
        self.cap = cap
        self.load_proc = load_proc
        self.size = 0
        self.buckets = [[] for _ in range(cap)]

    def _hash(self, key: str):
        h = 0
        for char in key:
            h = ((h * 31) + ord(char)) % self.cap
        return h

    def put(self, key: str, value: str):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if  k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.cap > self.load_proc:
            self._resize()

    def get(self, key: str): #По короткому коду возвращать исходную ссылку +
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return None

    def contains(self, key: str): #Проверка существования короткого кода +
        return self.get(key) is not None

    def remove(self, key: str):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def items(self): #Вывод всех сокращённых ссылок +
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result

    def _resize(self):
        new_cap = self.cap * 2
        old_buckets = self.buckets
        self.cap = new_cap
        self.buckets = [[] for _ in range(new_cap)]
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)


class CodeGenerator:
    def __init__(self, start=0):
        self.counter = start
        self.alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encode(self, num: int):
        if num == 0:
            return self.alphabet[0]
        result = []
        base = len(self.alphabet)
        while num > 0:
            result.append(self.alphabet[num % base])
            num //= base
        return ''.join(reversed(result))

    def next_code(self):
        code = self.encode(self.counter)
        self.counter += 1
        return code




