import argparse
import matplotlib.pyplot as plt
from PIL import Image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_img', help = 'Filename of source image')
    args = parser.parse_args()
    """
    impressionist = '{}_{}.jpg'.format(args.source_img, 'impressionist')
    expressionist = '{}_{}.jpg'.format(args.source_img, 'expressionist')
    coloristwash = '{}_{}.jpg'.format(args.source_img, 'coloristwash')
    pointillist = '{}_{}.jpg'.format(args.source_img, 'pointillist')
    
    impressionist_img = Image.open(impressionist)
    expressionist_img = Image.open(expressionist)
    coloristwash_img = Image.open(coloristwash)
    pointillist_img = Image.open(pointillist)

    fig, axs = plt.subplots(2, 2, figsize = (8, 6))
    
    axs[0][0].imshow(impressionist_img)
    axs[0][0].axis('off')
    axs[0][0].set_title('Impressionist')
    axs[0][1].imshow(expressionist_img)
    axs[0][1].axis('off')
    axs[0][1].set_title('Expressionist')
    axs[1][0].imshow(coloristwash_img)
    axs[1][0].axis('off')
    axs[1][0].set_title('Colorist Wash')
    axs[1][1].imshow(pointillist_img)
    axs[1][1].axis('off')
    axs[1][1].set_title('Pointillist')
    fig.tight_layout()

    plt.savefig('{}_all.jpg'.format(args.source_img))
    """

    output_8 = '{}_{}.jpg'.format(args.source_img, '8')
    output_4 = '{}_{}.jpg'.format(args.source_img, '4')
    output_2 = '{}_{}.jpg'.format(args.source_img, '2')

    src_img = Image.open('ntu_library.jpg')
    output_img_8 = Image.open(output_8)
    output_img_4 = Image.open(output_4)
    output_img_2 = Image.open(output_2)

    fig, axs = plt.subplots(1, 4, figsize = (10, 3))
    axs[0].imshow(src_img)
    axs[0].axis('off')
    axs[0].set_title('Orignial')
    
    axs[1].imshow(output_img_8)
    axs[1].axis('off')
    axs[1].set_title('Brush Size = 8')

    axs[2].imshow(output_img_4)
    axs[2].axis('off')
    axs[2].set_title('Brush Size = 4')

    axs[3].imshow(output_img_2)
    axs[3].axis('off')
    axs[3].set_title('Brush Size = 2')

    fig.tight_layout()
    plt.savefig('{}_process.jpg'.format(args.source_img))

