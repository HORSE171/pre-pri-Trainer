from flask import Flask, render_template, request
import random

app = Flask(__name__)

filename = "wordslova"
words = []
questions = []
questdict = {}


def loadFile():
    global words
    with open(filename, 'r', encoding="utf-8") as file:
        words = file.read().split("\n")


def createDict(words):
    questdict = {}
    for i in range(len(words)):
        word = words[i].lower()
        ind = word.find("пр")
        answer = word[ind + 2]
        word = word[:ind + 2] + "..." + word[ind + 3:]
        questdict.update({word: answer})
    return questdict


def generate_questions(questions_number):
    questions = words
    random.shuffle(questions)
    temp = []
    for i in range(questions_number):
        temp.append(questions[i])
    questdict = createDict(temp)
    return questdict


loadFile()


@app.route('/')  # привязка адреса к коду
def welcome():
    return render_template('welcome.html')

@app.route('/teoriya')  # привязка адреса к коду
def teoriya():
    return render_template('teoriya.html')

@app.route('/quiz', methods=['POST'])  # привязка адреса к коду
def quiz():
    global questdict
    number = request.form["qnum"]
    questdict = generate_questions(int(number))
    return render_template('main.html', questions=questdict)


@app.route('/results', methods=['POST'])
def check_answers():
    results = {}
    correct = 0
    for word in request.form:  # цикл по вопросам; входящая структура данных: {"вопрос":"буква которую ответил чел"}   requst.form ={'пр...любезный': 'е', 'пр...рвать': 'е', 'пр...мудрость': 'е', 'пр...валировать': 'е'}
        answered = request.form[word]  # сохраняем в вспомогательную переменную ответ(букву) на вопрос
        if questdict[word] == answered:  # сравнение буквы, которую ответил чел с правильной буквой в словаре вопросов
            correct = correct + 1  # если они равны то прибавляем 1 к переменной количества правильных ответов
            word = word.replace("...", questdict[word])
            results.update({word: True})
        else:
            word = word.replace("...", questdict[word])
            results.update({word: False})

    print(results)
    return render_template('results.html', correct=correct, results=results)


if __name__ == '__main__':
    app.run()
