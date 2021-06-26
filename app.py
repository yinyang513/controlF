import pytube
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def getWordAndURL():
    if request.method == 'POST':
        word = request.form.get('word')
        url = request.form.get('url')

        yt = pytube.YouTube(url)
        subt = yt.captions.get_by_language_code("en")
        sub = subt.generate_srt_captions().lower()
        subtitles = sub.split('\n')
        for x in range(len(subtitles)):
            subtitles[x] = subtitles[x].split(" ")
        time_stamps = []
        for x in range(len(subtitles)):
            for j in range(len(subtitles[x])):
                if subtitles[x][j] == word:
                    time_stamps.append(subtitles[x - 1][0][:-4])
        if not time_stamps:
            # print("Sorry! We could not find your word. :(")
            return render_template('controlf.html', name = 'Sorry! We could not find your word. :(')
        else:
            # print("Here are your time stamps:")
            # print('\n'.join(list(dict.fromkeys(time_stamps))))
            timestamps = list(dict.fromkeys(time_stamps))
            return render_template('controlf.html', name = 'Here are your time stamps:', timestamps = timestamps)
    else:
        return render_template('controlf.html',form = True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)