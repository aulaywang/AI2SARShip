import cv2
import os
 
videos_src_path = 'video_raw/'#提取图片的视频文件夹
videos_save_path = 'video_jpg/'#保存图片的路径
 
videos = os.listdir(videos_src_path) #用于返回指定的文件夹包含的文件或文件夹的名字的列表。
videos = filter(lambda x: x.endswith('mp4'), videos)#将flv文件读进来，可改为avi等格式
 
for each_video in videos:
    frame_count = 1
    # 得到每个文件夹的名字, 并指定每一帧的保存路径
    each_video_name, _ = each_video.split('.')
    os.mkdir(videos_save_path + '/' + each_video_name)
    each_video_save_full_path = os.path.join(videos_save_path, each_video_name) + '/'
 
    # 得到完整的视频路径
    each_video_full_path = os.path.join(videos_src_path, each_video)
    # 用OpenCV一帧一帧读取出来
    cap = cv2.VideoCapture(each_video_full_path)
    
    success = True
    while (success):
        success, frame = cap.read()
        print('Read a new frame: ', success)
        params = []
        params.append(1)
        #if len(frame) > 0:
        #if success:
        if frame is not None and frame_count<10:#每1帧取一帧图片保存下来，可以自己修改
            #cv2.imwrite(each_video_save_full_path + each_video_name + "%s.jpg" % frame_count, frame, str(str(0)*6 + str(frame)))
            cv2.imwrite(each_video_save_full_path +   "00000%d.jpg" % frame_count, frame, params)
            print(frame_count)
        elif frame is not None and frame_count<100:
            #cv2.imwrite(each_video_save_full_path + each_video_name + "%s.jpg" % frame_count, frame, str(str(0)*6 + str(frame)))
            cv2.imwrite(each_video_save_full_path +   "0000%d.jpg" % frame_count, frame, params)
            print(frame_count)
        elif frame is not None and frame_count<1000:
            #cv2.imwrite(each_video_save_full_path + each_video_name + "%s.jpg" % frame_count, frame, str(str(0)*6 + str(frame)))
            cv2.imwrite(each_video_save_full_path +   "000%d.jpg" % frame_count, frame, params)
            print(frame_count)
        elif frame is not None and frame_count<10000:
            #cv2.imwrite(each_video_save_full_path + each_video_name + "%s.jpg" % frame_count, frame, str(str(0)*6 + str(frame)))
            cv2.imwrite(each_video_save_full_path +   "00%d.jpg" % frame_count, frame, params)
            print(frame_count)
        elif frame is not None and frame_count<100000:
            #cv2.imwrite(each_video_save_full_path + each_video_name + "%s.jpg" % frame_count, frame, str(str(0)*6 + str(frame)))
            cv2.imwrite(each_video_save_full_path +   "0%d.jpg" % frame_count, frame, params)
            print(frame_count)
        frame_count = frame_count + 1
    cap.release()
