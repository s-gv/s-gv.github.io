import random
import numpy as np
import os
from PIL import Image, ImageDraw
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Conv2D, Dense, Reshape, Lambda, GlobalAveragePooling2D, MaxPooling2D, RepeatVector
from tensorflow.keras import backend as K
import tensorflow_probability as tfp

emoji_img = Image.open('data/emoji_0045.png').convert('L').resize((9, 9), resample=Image.BILINEAR)
emoji_w, emoji_h = emoji_img.size

def gen_data(dx=2, dy=0):
    img_w, img_h = 32, 32
    bg_color = random.randint(0, 10)
    sq_color = random.randint(240, 255)

    img_x = Image.new('L', (img_w, img_h), color=bg_color)
    img_y = Image.new('L', (img_w, img_h), color=bg_color)

    sz = 5
    cx, cy = random.randint(2*sz, img_w//2), random.randint(2*sz, img_h-2*sz)
    dx = random.choice([2, 3])
    
    draw_x = ImageDraw.Draw(img_x)
    draw_y = ImageDraw.Draw(img_y)

    draw_x.rectangle([(cx - sz//2, cy - sz//2), (cx + sz//2, cy + sz//2)], fill=sq_color)
    draw_y.rectangle([(cx - sz//2 + dx, cy - sz//2 + dy), (cx + sz//2 + dx, cy + sz//2 + dy)], fill=sq_color)

    #img_x.paste(emoji_img, box=(cx - emoji_w//2, cy - emoji_h//2))
    #img_y.paste(emoji_img, box=(cx - emoji_w//2 + dx, cy - emoji_h//2 + dy))

    x = np.array(img_x).reshape((img_h, img_w, 1)).astype(np.float32) / 255.0
    y = np.array(img_y).reshape((img_h, img_w, 1)).astype(np.float32) / 255.0

    return x, y

def w_init(shape, dtype=None):
    w = np.array([
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
    ], dtype=np.float32)
    w = w.reshape((3, 7, 7, 1, 1)).transpose(-1, 1, 2, 3, 0)[0]
    return w
    #return K.random_normal(shape, dtype=dtype)

enc_ip = Input(shape=(32, 32, 2))
enc_op = Sequential([
    Conv2D(8, (9, 9), padding='same', activation='relu'),
    MaxPooling2D(2),
    Conv2D(16, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(2),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(2),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    GlobalAveragePooling2D(),
    Dense(2),
])(enc_ip)
encoder = Model(inputs=[enc_ip], outputs=[enc_op])


dec_ip, l_ip, t_ip = Input(shape=(32, 32, 1)), Input(shape=(2,)), Input(shape=(1,))
filt_x = Conv2D(3, (7, 7), padding='same', use_bias=False, kernel_initializer=w_init, name='filts')(dec_ip)
gumbel_dist = tfp.distributions.RelaxedOneHotCategorical(logits=l_ip, temperature=t_ip[0])
samples = gumbel_dist.sample()
g_s = Dense(2)(samples)
r = Sequential([
    RepeatVector(1024),
    Reshape((32, 32, 2))
])(g_s)
f = Sequential([
    Conv2D(512, (9, 9), padding='same', activation='relu'),
    Conv2D(8, (1, 1), padding='same', activation='relu'),
])(dec_ip)
fr = tf.keras.layers.concatenate([f, r])
fo = Conv2D(3, (1, 1), padding='same', activation='softmax')(fr)
filt_x_attn = tf.keras.layers.multiply([fo, filt_x])
dec_op = Lambda(lambda x: K.sum(x, axis=(-1,), keepdims=True))(filt_x_attn)
decoder = Model(inputs=[dec_ip, l_ip, t_ip], outputs=[dec_op])
#decoder.get_layer('filts').trainable = False


combined_ip, combined_post_ip, combined_t_ip = Input(shape=(32, 32, 1)), Input(shape=(32, 32, 1)), Input(batch_shape=(1,))
r_logits = encoder(tf.keras.layers.concatenate([combined_ip, combined_post_ip]))
combined_op = decoder([combined_ip, r_logits, combined_t_ip])
model = Model(inputs=[combined_ip, combined_post_ip, combined_t_ip], outputs=[combined_op])
model.compile(tf.keras.optimizers.Adam(lr=3e-4), loss='mse')


def main():
    x_train, y_train = [], []
    for _ in range(10000):
        x_t, y_t = gen_data()
        x_train.append(x_t)
        y_train.append(y_t)

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    # hacky way to anneal temperature
    model.fit([x_train, y_train, np.array([0.25]*x_train.shape[0])], [y_train], epochs=5, batch_size=64)
    model.fit([x_train, y_train, np.array([0.10]*x_train.shape[0])], [y_train], epochs=5, batch_size=64)
    model.fit([x_train, y_train, np.array([0.05]*x_train.shape[0])], [y_train], epochs=20, batch_size=64)
   
    '''
    with np.printoptions(precision=3, suppress=True):
        w = model.get_layer('filts').get_weights()[0]
        print(w.shape)
        print(w[:, :, 0, 0])
        print(w[:, :, 0, 1])
        print(w[:, :, 0, 2])
    '''

    test_x, test_y = gen_data()
    test_yp = decoder.predict([test_x[None], np.array([[0., 0.]]), np.array([0.05])])
    
    os.system('rm -f tmp/*.png')
    Image.fromarray((test_x*255).astype(np.uint8).squeeze()).save('tmp/test_x.png')
    Image.fromarray((test_y*255).astype(np.uint8).squeeze()).save('tmp/test_y.png')
    Image.fromarray((test_yp*255).astype(np.uint8).squeeze()).save('tmp/test_yp.png')

    for i in range(5):
        test_yp = decoder.predict([test_yp, np.array([[0., 0.]]), np.array([0.05])])
        Image.fromarray((test_yp*255).astype(np.uint8).squeeze()).save(f'tmp/test_yp_{i}.png')




if __name__ == '__main__':
    main()
