# Promptenhance

A web app to provide a top-down, template view for image and video generation. 
* Generate an image.
* Generate another image.
* Combine the two images.
* Turn the combined image into a video with the prompt used to generate it.

Leveraging the following APIs, all via [Fal.ai](https://fal.ai/dashboard):
* [Google DeepMind](https://deepmind.google/) [Imagen 4](https://fal.ai/models/fal-ai/imagen4/preview) for images.
* [Kling](https://kling.ai/) [2.1](https://fal.ai/models/fal-ai/kling-video/v2.1/master/image-to-video) for video.
* [Fal's](https://fal.ai/dashboard) own [video prompt generator](https://fal.ai/models/fal-ai/video-prompt-generator) to get the ball rolling on prompts, giving Promptenhance its name. Using AI *in addition to* (never *instead of*) creativity.

![](images/promptenhance.png)

[Web app demo](https://youtu.be/mxB0_Cnp5eE) | [Click here to view *Realm of the Kingdom*](https://youtu.be/ZPXR_SzOJKs), a short film created with Promptenhance.

![](images/rotk.jpg)

## Setup

Be sure to use a virtual environment:
> ```sh
> $ python3 -m venv venv
> ```
(Here, `venv` is just an example, the virtual environment can be given *any* name).

Activate the virtual environment:
> ```sh
> $ source venv/bin/activate
> ```

Upon activation, run `pip list`. Only `pip` and `setuptools` should be installed in the virtual environment.

Install requirements:
> ```sh
> $ pip install -r requirements.txt
> ```

Create .env:
> ```sh
> $ touch .env
> ```

Create [Fal.ai](https://fal.ai/dashboard) API key [here](https://fal.ai/dashboard/keys).

Add `FAL_KEY="[FAL_KEY]"` to `.env`.

Add `**/.env` to `.gitignore`.

Run the app:
> ```sh
> $ streamlit run app.py
> ```

The app will be live at `http://localhost:8501`.

## To-do

- Add drop-down menus for:
    - Different image models.
    - Different video models.
    - Aspect ratio (for both image and video).
- Add duration option to video.
- Add option for negative prompts.
- Add prompt history.
- Work on a more elaborate frontend. ([Streamlit](https://streamlit.io/) is ideal for prototyping, but not the most presentable):
    - On a related note, refactor the code. As of this writing, the entire app is one `.py` file.
