import torchvision.transforms as T

def get_augmentations(train: bool = True) -> T.Compose:
	if train:
		transformer = T.Compose([
			T.Resize(size=(224, 224)),
			T.RandomRotation(degrees=(0, 180)),
			T.ToTensor(),
			T.Normalize(mean=0, std=1)
    	])
	else:
		transformer = T.Compose([
			T.Resize(size=(224, 224)),
			T.ToTensor(),
			T.Normalize(mean=0, std=1)
		])

	return transformer
