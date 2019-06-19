## git

tag 就是提交的别名，和branch无关系

    1.在本地的分支当中操作，先只有master分支，然后git tag v0.1,再git checkout -b dev切换到dev分支，在dev分支下也可以看到tag
    
    2.在本地的分支当中操作，先只有master，然后git checkout -b dev, 在dev分支下再git tag v0.1,再切换到master分支，仍然可以看到tag.
    
    在多个分支的情况下，在不同分支下git tag添加的分支在其他分支是可以看到的, 任何时候git tag看到的都是全局的tag, 即使把创建tag时等待分支
    删除了，tag也还存在。
    
    在本地分支打的tag默认不会push到远端，需要显式提交 git push origin –tags # 将本地所有标签一次性提交到git服务器

分支：
    
    在git clone之后，Git 会自动将此远程仓库命名为origin,origin只相当于一个别名，运行git remote –v或者查看.git/config可以看到origin的含义,
    用(远程仓库名/分支名) 这样的形式表示远程分支，所以origin/master指向的是一个remote branch， 这只是远程分支的别名， 真实的远程分支需要IP地址
    git remote -v
    origin	git@192.168.70.8:test.git (fetch)   # 表示origin关联到的仓库，作为拉取代码用
    origin	git@192.168.70.8:test.git (push)    # 推送代码用
    
    git本地仓库关联远程仓库的两种方式：
    1.将远程的代码clone到本地仓库 
    2.将本地的代码手动关联到远程仓库，可以关联到多个远程仓库，默认第一个是origin，其他仓库用其他名字用于区分
    git remote add origin git@github.com:hackenzheng/test.git 关联到本地仓库，本地仓库的别名是origin也可以用其他，真实地址是git@github.com...

git其他操作：

    git remote prune origin   # 跟新远端分支信息
    git checkout -b  test  会以当前分支建立一个新分支test并切换过去
    git branch test  #是从本地当前分支检出来的，而不是从远端
    git checkout origin/dev1.0 -b test  #切换到远端dev1.0分支，并在本地创建test分支关联到远端，一定要在本地新建个分支与远端关联，本地分支只能关联一个远端分支，不能切换远端分支
    

## raw.githubusercontent.com与github的关系
raw.githubusercontent.com是github用来存储用户上传文件（不是项目仓库的文件，而是issue里的图片之类的）的服务地址。放在亚马逊s3上。
是github 的素材服务器, 避免跟主服务抢占负载。两者除了最开始的位置，后面的文件夹路径都一样。

比如一个readme.md文件，如果直接wget https://github.com/xx/xx/readme.md,保存下来的是个html文件，是经过渲染之后的。
如果只要保存readme.md文件本身，就用https://raw.githubusercontent.com/xx/xx/readme.md这个路径.