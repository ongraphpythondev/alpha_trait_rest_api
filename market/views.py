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
        except Exception as e:
            return JsonResponse({}, status=400)

        logo_byte, background_byte = convert_image_to_bytes(logo), convert_image_to_bytes(background_image)
        template_dir = 'MarketTemplate'
        market_templates_list = os.listdir(str(settings.BASE_DIR) + '/templates/' + template_dir)
        market_images_list = []
        for temp in market_templates_list:
            print(temp)
            template_path = template_dir+f"/{temp}"
            template = get_template(template_path)

            context = {"logo": logo_byte, "bg_image": background_byte, "text": text, "head_color":head_color, "foot_color": foot_color, "frame_color": frame_color}

            html = template.render(context)
            save_images(html, f'{temp.split(".")[0]}.png', type=market_hti)
            market_images_list.append('http://127.0.0.1:8000'+market_static_path+f'{temp.split(".")[0]}.png')
        return JsonResponse({"images": market_images_list}, status=200)
