import qrcode
import os
from django.conf import settings
from django.shortcuts import render
from django.utils.crypto import get_random_string


def qr_generator_view(request):
    qr_image_url = None
    form_data = {
        'message': '',
        'link': '',
        'box_size': '10',
        'border': '1',
        'fill_color': '#000000',   
        'back_color': '#ffffff',
        'display_mode': 'both',
    }

    if request.method == 'POST':
        form_data['message'] = request.POST.get('message', '')
        form_data['link'] = request.POST.get('link', '').strip()
        form_data['box_size'] = request.POST.get('box_size', '10')
        form_data['border'] = request.POST.get('border', '4')
        form_data['fill_color'] = request.POST.get('fill_color', '#000000')
        form_data['back_color'] = request.POST.get('back_color', '#ffffff')
        form_data['display_mode'] = request.POST.get('display_mode', 'both')

        message = form_data['message']
        link = form_data['link']
        display_mode = form_data['display_mode']

        if display_mode == 'message':
            qr_content = message
        elif display_mode == 'url':
            qr_content = link
        else:
            qr_content = f"{message}\n{link}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=int(form_data['box_size']),
            border=int(form_data['border']),
        )
        qr.add_data(qr_content)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=form_data['fill_color'],
            back_color=form_data['back_color']
        )

        filename = f"qr_{get_random_string(8)}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        img.save(file_path)
        qr_image_url = settings.MEDIA_URL + filename

    return render(request, 'generator.html', {
        'qr_image_url': qr_image_url,
        'form_data': form_data,
    })
