# promptenhance

A web app to provide a more top-down view of the various stages of video generation.

## Setup

Be sure to use a virtual environment:
> ```sh
> $ python3 -m venv venv
> ```
Here, `venv` is just an example, the virtual environment can be given *any* name.

To activate the virtual environment, run the following command:
> ```sh
> $ source venv/bin/activate
> ```

Upon activation, run `pip list`. Only `pip` and `setuptools` should be installed in the virtual environment.

To install requirements, run:
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

## To-do

- Add drop-down menus for:
    - Image generation models.
    - Video generation models.
    - Aspect ratio (for both image and video).
    - Add duration option to video.
- Work on a more elaborate frontend. ([Streamlit](https://streamlit.io/) is ideal for prototyping, but not the most presentable).
