# Voice Your Professional Email

This project was worked on during the BoilerMake 2018 Hackathon. 

It basically asks the users a bunch of questions and stores the answers. These answers are used to tailor make a professional email for a student to write to their professor. 

We understand that writing a good professional email can be a difficult task and make you lose opportunities if not well written, hence we planned on tackling that issue at the basic student-professor level.

## Group Members:
- Tej Patel
- Eric Chheang
- Joshua Baunach

## Setup

Ensure Python, Pip, and Virtualenv are installed.

Run the following command

```
.\Boilermake2018\Srcipts\Acrivate
```

## Running

Open two terminal windows. In the first window, run the following command:

```
npm run
```
This will start the Electron frontend.

In the other window, run the following command:

```
python main.py
```

From there, click on "Start Process!" in the Electron window. It will ask you for something. Say the following exactly:

"I need help writing a professional email."

After that, just follow its prompts.

Once it is done, it will write the results to output/professional_email.txt.
