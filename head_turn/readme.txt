D:\repo\posts\head_turn>python detect_head_turn.py -i left.jpg
Found 1 face(s) in this photograph.
red / green = 3.3, turned left
saved to out_left.jpg

D:\repo\posts\head_turn>python detect_head_turn.py -i right.jpg 
Found 1 face(s) in this photograph.
green / red = 3.4, turned right
saved to out_right.jpg

D:\repo\posts\head_turn>python detect_head_turn.py -i straight.jpg
Found 1 face(s) in this photograph.
red / green = 1.0, facing straight
saved to out_straight.jpg



   On Ubuntu/Debian systems:
   ```
   sudo apt-get install ttf-mscorefonts-installer
   ```

   On CentOS/Red Hat systems:
   ```
   sudo yum install msttcore-fonts-installer
   ```

   After installation, you may have to update the font cache:
   ```
   sudo fc-cache -f -v



   5. **Update the script to use a different font**:
   You might decide to simply use a font that you know exists on your system. For example, many Linux systems come with the DejaVu fonts installed:
   ```python
   font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=font_size)