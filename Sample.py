from huggingface_hub import from_pretrained_fastai
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

learn = from_pretrained_fastai("sacamiso/crops")
print(learn.predict("cover-crops.png"))