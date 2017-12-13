from flask import Flask, render_template
app = Flask(__name__)
 
@app.route('/')
def index(): 
	return render_template('home.html')

@app.route('/user/<user>')
def channel(user):
	return render_template('user.html',data=data)

@app.route('/<blogpost>')
def view_post(blogpost):
	return render_template('blogpost.html',data=blogpost)

	


if __name__ == '__main__':
	app.run(debug=True)