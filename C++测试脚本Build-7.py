try:
    import time as ti
    import os
    import subprocess as sb
    import glob
    import shutil as sh
    print("C++测试器  HelloWorldCoder(-China)制作  你只拥有此软件的永久使用、复制权\n详见软件目录下的LICENSE文件")
    programdir=os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("你可以在{}下创建Tester.set配置文件".format(os.path.dirname(os.path.abspath(__file__))))
    filedset=False
    try:
        with open("Tester.set","r",encoding="utf-8") as setting:
            print("[Loading Setting]")
            setting_data=setting.readline()
            settings=setting_data.split(";")
            print(settings)
            path=settings[0]
            linesdefult=int(settings[1])
            timebetwin=float(settings[2])
            optype=settings[3]
            ignore_end_n=settings[4]
            run_file=int(settings[5])
            if run_file==1:
                time_limit=float(settings[6])
                file_name=settings[7]
                if optype=="2":
                    points=int(settings[8])
            else:
                file_name=settings[6]
                if optype=="2":
                    points=int(settings[7])
            filedset=True
            print("[Setting Loaded]")
    except FileNotFoundError:
        pass
    if not filedset:
        path=input("测试目录：")
    os.chdir(path)
    if not filedset:
        linesdefult=int(input("测试行数，0为无限测，-1为自动决定："))
        lines=linesdefult
        timebetwin=float(input("测试时间间隔："))
        optype=input("请选择操作：输入1进行单次测试，输入2进行多次测试，输入其他退出：")
        ignore_end_n=input("是否要忽略末尾换行符(Y/N，务必大写)：")
        run_file=int(input("是否需要编译、运行C++文件？输入1编译、运行，输入2不编译、不运行："))
        if run_file==1:
            time_limit=float(input("请输入时间限制："))
    if optype=="1":
        pass_this=False
        if not filedset:
            file_name=input("测试文件名：")
        if run_file==1:
            print("[Compileting]")
            os.system("cd {} && g++ -o {}-test {}.cpp".format(path,file_name,file_name))
            print("[Running]")
            comprogpath=glob.glob(path+"/"+file_name+"-test*",recursive=True)[0]
            output=open(path+"/"+file_name+".out","w+",encoding="utf-8")
            input_=open(path+"/"+file_name+".in","r+",encoding="utf-8")
            error_=open(path+"/"+file_name+".ERR","w+",encoding="utf-8")
            try:
                testerp=sb.Popen(args=comprogpath,stderr=error_,stdin=input_,stdout=output)
                testerp.wait(time_limit)
            except sb.TimeoutExpired:
                print("[TLE]Time Limit Exceeded")
                flag=False
                pass_this=True
            output.close()
            error_.close()
            input_.close()
            print("[Testing]")
        answer=open(path+"/"+file_name+".ans","r+",encoding="utf-8")
        if linesdefult==-1:
            lines=len(answer.readlines())
            answer.seek(0)
        try:
            output=open(path+"/"+file_name+".out","r+",encoding="utf-8")
        except FileNotFoundError:
            print("[Error]Output File Not Found!")
            flag=False
            pass_this=True
        point_w=0
        point_r=0
        if not pass_this:
            line_No=1
            flag=True
            while line_No<=lines or linesdefult==0:
                ansline=answer.readline()
                outputline=output.readline()
                if ignore_end_n=="Y" and line_No==lines:
                    ansline=ansline.split("\n")[0]
                    outputline=outputline.split("\n")[0]
                if ansline==outputline:
                    print("[Test Line: {}] Answer: [{}]  Program Output: [{}]  Test End Type: [Passed]".format(line_No,ansline,outputline))
                    point_w+=1
                else:
                    print("[Test Line: {}] Answer: [{}]  Program Output: [{}]  Test End Type: [Failed]".format(line_No,ansline,outputline))
                    point_r+=1
                    flag=False
                line_No+=1
                ti.sleep(timebetwin)
        if flag:
            print("[Test Finished] Total End Type: [Passed]")
        else:
            print("[Test Finished] Total End Type: [Failed] ={} Lines Right  {} Lines Wrong=".format(point_w,point_r))
    elif optype=="2":
        if not filedset:
            file_name=input("测试文件名格式（填序号的位置用{}替代，如：abc[1]->abc[{}],abc1->abc{}）：")
            points=int(input("请输入样例点总数："))
        flag1=True
        big_r=0
        big_w=0
        if run_file==1:
            print("[Compileting Program]File Name：{}".format(file_name.format("")))
            os.system("cd {} && g++ -o {}-test {}.cpp".format(path+"/",file_name.format(""),path+"/"+file_name.format("")))
        for i in range(1,points+1):
            pass_this=False
            if run_file==1:
                print("[Creating Test Point Dictionary]Test Point：{}".format(i))
                os.makedirs(path+"/testpoint"+str(i),exist_ok=True)
                os.chdir(path+"/testpoint"+str(i))
                print("[Copying Test Point Files]Test Point：{}".format(i))
                comprogpath=glob.glob(path+"/"+file_name.format("")+"-test*",recursive=True)[0]
                sh.copy2(comprogpath,path+"/testpoint"+str(i)+"/"+os.path.basename(comprogpath))
                sh.copy2(path+"/"+file_name.format(i)+".ans",path+"/testpoint"+str(i)+"/"+file_name.format("")+".ans")
                sh.copy2(path+"/"+file_name.format(i)+".in",path+"/testpoint"+str(i)+"/"+file_name.format("")+".in")
                print("[Running Test Point]Test Point：{}".format(i))
                output=open(path+"/testpoint"+str(i)+"/"+file_name.format("")+".out","w+",encoding="utf-8")
                input_=open(path+"/testpoint"+str(i)+"/"+file_name.format("")+".in","r+",encoding="utf-8")
                error_=open(path+"/testpoint"+str(i)+"/"+file_name.format("")+".ERR","w+",encoding="utf-8")
                try:
                    testerp=sb.Popen(args=path+"/testpoint"+str(i)+"/"+os.path.basename(comprogpath),stderr=error_,stdin=input_,stdout=output)
                    testerp.wait(time_limit)
                except sb.TimeoutExpired:
                    print("[TLE]Time Limit Exceeded")
                    flag=False
                    pass_this=True
                output.close()
                error_.close()
                input_.close()
                answer=open(path+"/testpoint"+str(i)+"/"+file_name.format("")+".ans","r+",encoding="utf-8")
                if linesdefult==-1:
                    lines=len(answer.readlines())
                    answer.seek(0)
                try:
                    output=open(path+"/testpoint"+str(i)+"/"+file_name.format("")+".out","r+",encoding="utf-8")
                except FileNotFoundError:
                    print("[Error]Output File Not Found!")
                    flag=False
                    pass_this=True
                print("[Testing Test Point]Test Point：{}".format(i))
            else:
                answer=open(path+"/"+file_name.format(i)+".ans","r+",encoding="utf-8")
                output=open(path+"/"+file_name.format(i)+".out","r+",encoding="utf-8")
            point_r=0
            point_w=0
            if not pass_this:
                line_No=1
                flag=True
                while line_No<=lines or linesdefult==0:
                    ansline=answer.readline()
                    outputline=output.readline()
                    if ignore_end_n=="Y" and line_No==lines:
                        ansline=ansline.split("\n")[0]
                        outputline=outputline.split("\n")[0]
                    if ansline==outputline:
                        print("[Point: {}][Test Line: {}] Answer: [{}]  Program Output: [{}]  Test End Type: [Passed]".format(i,line_No,ansline,outputline))
                        point_w+=1
                    else:
                        print("[Point: {}][Test Line: {}] Answer: [{}]  Program Output: [{}]  Test End Type: [Failed]".format(i,line_No,ansline,outputline))
                        point_r+=1
                        flag=False
                    line_No+=1
                    ti.sleep(timebetwin)
            if flag:
                print("[Point: {}][Test Finished] Total End Type: [Passed]".format(i))
                big_r+=1
            else:
                print("[Point: {}][Test Finished] Total End Type: [Failed] ={} Lines Right  {} Lines Wrong=".format(i,point_w,point_r))
                big_w+=1
                flag1=False
        if flag1:
            print("[Test Finished] Total End Type: [Passed]")
        else:
            print("[Test Finished] Total End Type: [Failed] ={} Points Right  {} Points Wrong=".format(big_r,big_w))
except:
    print("[Error] 程序出现错误，请检查输入是否有误、路径是否有空格、文件是否备全、配置文件是否正确\n检查后仍无法解决，请在GitHub上提交Issue反馈，最好附截图，谢谢！！")
finally:
    input("按Enter以退出.....")