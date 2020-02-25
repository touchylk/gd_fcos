# coding:utf-8
import os
import cv2
import sys
import shutil
# from fcos_core.data.datasets.gd import GDDataset
if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET
split = 'train'
img_dir = f'/media/e813/E/dataset/flag_k/{split}_nonomal_images/'
anno_dir = f'/media/e813/E/dataset/flag_k/{split}_nonomal_annos/'
backupdir = '/media/e813/E/dataset/flag_k/backup/'
imgnamelist = os.listdir(img_dir)
imgnamelist.sort()
classdict ={}
for imgname in imgnamelist:
    purname = imgname.split('.')[0]
    xmlname = purname+'.xml'
    imgpath = os.path.join(img_dir,imgname)
    xmlpath = os.path.join(anno_dir,xmlname)
    # img = cv2.imread(imgpath)
    try:
        anno = ET.parse(xmlpath).getroot()
    except:
        print(xmlpath,1)
        shutil.copyfile(imgpath,os.path.join(backupdir,imgname))
        shutil.copyfile(xmlpath, os.path.join(backupdir, xmlname))
        os.remove(imgpath)
        os.remove(xmlpath)
        continue
    for obj in anno.iter("object"):
        difficult = int(obj.find("difficult").text) == 1

        name = obj.find("name").text.lower().strip()
        if name=='normal_flag':
            print(xmlpath)
        bb = obj.find("bndbox")
        # Make pixel indexes 0-based
        # Refer to "https://github.com/rbgirshick/py-faster-rcnn/blob/master/lib/datasets/pascal_voc.py#L208-L211"
        try:
            box = [
                bb.find("xmin").text,
                bb.find("ymin").text,
                bb.find("xmax").text,
                bb.find("ymax").text,
            ]
        except:
            print(xmlpath,bb)
            shutil.copyfile(imgpath, os.path.join(backupdir, imgname))
            shutil.copyfile(xmlpath, os.path.join(backupdir, xmlname))
            os.remove(imgpath)
            os.remove(xmlpath)
            continue
        box = [int(x) for x in box]
        # cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),color=255,thickness=1)
        # print(name)
        if name  not in classdict:
            classdict[name]=1
        else:
            classdict[name]+=1
        # bndbox = tuple(
        #     map(lambda x: x - TO_REMOVE, list(map(int, box)))
        # )
        #
        # boxes.append(bndbox)
        # gt_classes.append(self.class_to_ind[name])
        # difficult_boxes.append(difficult)
    #
    # size = target.find("size")
    # im_info = tuple(map(int, (size.find("height").text, size.find("width").text)))
    #
    # res = {
    #     "boxes": torch.tensor(boxes, dtype=torch.float32),
    #     "labels": torch.tensor(gt_classes),
    #     "difficult": torch.tensor(difficult_boxes),
    #     "im_info": im_info,
    # }
    # cv2.imshow(imgname,img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
print(classdict)