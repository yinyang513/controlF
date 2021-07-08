import pytube
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def getWordAndURL():
    if request.method == 'POST':
        word = request.form.get('word')
        url = request.form.get('utube') # include mp4 videos and implement with speech to text api

        yt = pytube.YouTube(url)
        subt = yt.captions.get_by_language_code("en") #add more caption languages
        sub = subt.generate_srt_captions().lower()
        subtitles = sub.split('\n')
        for x in range(len(subtitles)):
            subtitles[x] = subtitles[x].split(" ")
        time_stamps = []
        for x in range(len(subtitles)): # finding word
            for j in range(len(subtitles[x])):
                if subtitles[x][j] == word:
                    time_stamps.append(subtitles[x - 1][0][:-4])
        if not time_stamps:
            return render_template('controlf.html', name = 'Sorry! We could not find your word. :(', back = True)
        else:
            links = []
            timestamps = list(dict.fromkeys(time_stamps))
            for time in timestamps:
                split_time = time.split(':')
                second = int(split_time[0])*3600 + int(split_time[1])*60 + int(split_time[2])
                link_timestamps = url + "&t=" + str(second) + "s"
                links.append(link_timestamps)
            return render_template('controlf.html', name = 'Here are your time stamps:', links_timestamps = zip(links,timestamps), back = True)
    else:
        return render_template('controlf.html',form = True)

if __name__ == "__main__":
    app.run(port=5000, debug=True) 