import skimage.transform
import skimage.color
import skimage.data
import numpy as np
import cv2


def load_image(filename):
    im = skimage.img_as_float(skimage.io.imread(filename)).astype(np.float32)
    dims = np.shape(im)
    if dims[2] == 3:
        return im
    elif dims[2] == 1:
        ret = np.zeros((dims[0], dims[1], 3))
        for i in range(0,3):
            ret[:, :, i] = im
            return ret
    elif dims[2] > 3:
        return im[:, :, :3]
    else:
        raise ValueError('Image must have 1, 3 or 4 channels')


def resize_image(im, resize_size, mean_values=None):
    '''
    Resizes image and pads with the mean image if necessary (generates square image!)
    '''
    if mean_values is None:
        mean_img = (128./255) * np.ones((resize_size, resize_size, 3))
    else:
        mean_img = np.ones((resize_size, resize_size, 3))
        # Caffe works with BGR: (0,1,2) <-> (2,1,0)
        mean_img[:, :, 0] = (mean_values[2] / 255.) * mean_img[:, :, 0]
        mean_img[:, :, 1] = (mean_values[1] / 255.) * mean_img[:, :, 0]
        mean_img[:, :, 2] = (mean_values[0] / 255.) * mean_img[:, :, 0]
    # Find the largest side
    original_height, original_width = np.shape(im)[0], np.shape(im)[1]
    if original_height > original_width:
        scale_factor = 1.*resize_size/original_height
        new_height = resize_size
        new_width = int(scale_factor*original_width)
    else:
        scale_factor = 1. * resize_size / original_width
        new_width = resize_size
        new_height = int(scale_factor * original_height)

    # Perform the resize
    resized_image = skimage.transform.resize(im, (new_height, new_width))#, preserve_range=True)

    # Fill the result with the mean image and put the resized image on top of it
    res = np.copy(mean_img)
    center = int(resize_size/2)
    y0 = center-int(new_height/2)
    y1 = y0+new_height
    x0 = center-int(new_width/2)
    x1 = x0 + new_width
    res[y0:y1, x0:x1, :] = resized_image

    return res


def draw_bounding_box(video_path, filename, save_dir, pred_bounding_box, gt_bounding_box):
    img = cv2.imread(video_path+filename)
    x, y, w, h = pred_bounding_box
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    x, y, w, h = gt_bounding_box
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(save_dir + filename, img)
