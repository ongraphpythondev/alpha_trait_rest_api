import base64, os

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import get_template
from rest_framework.views import APIView

from html2image import Html2Image


# Create your views here.

market_static_path = '/static/market/marketImages/'
advertisement_static_path = '/static/advertisement/advertisementImages/'

market_hti = Html2Image(output_path=str(settings.BASE_DIR) + market_static_path)
advertisement_hti = Html2Image(output_path=str(settings.BASE_DIR) + advertisement_static_path)





def save_images(html, file_name, type):
    eval('type.screenshot(html_str=html, save_as=file_name)')
    return True

def convert_image_to_bytes(img):
    return base64.b64encode(img.read()).decode("utf-8")



class MarketImage(APIView):
    def post(self, request):
        """
        input params:
            head_color       ==> string
            background_image ==> file
            logo             ==> file
            text             ==> string
            text_color       ==> string
            foot_color       ==> string
        """
        try:
            head_color = request.POST['head_color']
            background_image = request.FILES['background_image']
            logo = request.FILES['logo']
            text = request.POST['text']
            frame_color = request.POST['frame_color']
            foot_color = request.POST['foot_color']
            template_number = request.POST['template_number']
            font = request.POST['font_name']
            width = request.POST['width']
            height = request.POST['height']
        except Exception as e:
            print(e)
            return JsonResponse({}, status=400)

        logo_byte, background_byte = convert_image_to_bytes(logo), convert_image_to_bytes(background_image)

        template_dir = 'MarketTemplate'
        temp = f"template-{template_number}.html"
        template_path = template_dir+f"/{temp}"
    
        try:
            template = get_template(template_path)
        except Exception:
            return JsonResponse({"message": "Template doesn't exists"}, status=400)

        google_font_name = "+".join(font.strip().split(" ")) 

        context = {
            "logo": logo_byte, 
            "bg_image": background_byte, 
            "text": text, 
            "head_color":head_color, 
            "foot_color": foot_color, 
            "frame_color": frame_color, 
            "font_family": font, 
            "google_font_name": google_font_name.title(),
            "height1": height,
            "width1": width
        }

        html = template.render(context)
        market_images_list = []
        # print(html)
        print(height)
        save_images(html, f'{temp.split(".")[0]}.png', type=market_hti)

        market_images_list.append('http://127.0.0.1:8000'+market_static_path+f'{temp.split(".")[0]}.png')

        return JsonResponse({"images": market_images_list}, status=200)
