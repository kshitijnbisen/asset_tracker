import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import AssetType, Item, AssetImage
from .forms import AssetTypeForm, ItemForm, AssetImageForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
import csv
# Create your views here.


@login_required(redirect_field_name='login', login_url='/account/login/')
def dashboard_view(request):
    """
    It renders a index page
    """
    bar_label = ['Active Assets', 'Inactive Assets']
    item_detail = Item.objects.values('is_active').order_by().annotate(Count('item_id'))
    bar_data = []
    for count in item_detail:
        bar_data.append(count['item_id__count'])

    pie_label = []
    queryset = AssetType.objects.all().order_by('asset_type')
    for asset in queryset:
        pie_label.append(asset.asset_type)
    pie_data = []
    data = Item.objects.values('asset_type').order_by('asset_type').annotate(Count('asset_type'))
    for asset_count in data:
        pie_data.append(asset_count['asset_type__count'])
    context = {'bar_label': bar_label, 'bar_data': bar_data, "pie_label": pie_label, "pie_data": pie_data}
    return render(request, 'assetmaster/dashboard2.html', context)

def all_assettype_view(request):
    """
    This function fetch all the data from AssetType table.

    Parameters:
    arg1 (): HttpRequest Object

    Returns:
    dict: all the AssetType object

    """
    assettype = AssetType.objects.all()
    context = {'assettype': assettype}
    return render(request, 'assetmaster/all_assettype.html', context)


def add_assettype_view(request):
    """
    This function adds new data to  AssetType table.

    Parameters:
    arg1 (): HttpRequest Object(with asset_type(str),asset_description(str))

    Returns:
    dict: AssetType object
    msg: 'AssetType Added Successfully!' | msg: 'Something went wrong!'

    """
    form = AssetTypeForm()
    my_dict = {'form': form}
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'AssetType Added Successfully!')
            return redirect('/all_category')
        else:
            messages.error(request, 'Something went wrong!')
            return render(request,'assetmaster/add_assettype.html', my_dict)
    return render(request,'assetmaster/add_assettype.html', my_dict)


def update_assettype_view(request, id):
    """
    This data update data from AssetType table.

    Parameters:
    arg1 ():
    arg2 (int): id of object

    Returns:
    msg: 'Assettype updated Sucessfully!'

    """
    assettype = AssetType.objects.get(id=id)
    if request.method == 'POST':
        form = AssetTypeForm(request.POST, instance=assettype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assettype updated Successfully!')
            return HttpResponseRedirect('/all_category')
    else:
        form = AssetTypeForm(instance=assettype)
    context = {'form': form}
    return render(request, 'assetmaster/update_assettype.html', context )

def remove_assettype_view(request, id):
    """
    This function deletes data from AssetType table.

    Parameters:
    arg1 ():
    arg2 (int): id of object

    Returns:
    None: None

    """
    at_to_be_removed = AssetType.objects.get(id=id)
    at_to_be_removed.delete()
    messages.success(request, 'Assettype deleted Sucessfully!')
    return redirect('/all_category')


def all_items_view(request):
    """
    This function fetch all the data from Item table.

    Parameters:
    arg1 (): None

    Returns:
    dict: all the Items object

    """
    items = Item.objects.all().order_by('-updated_at')
    paginator = Paginator(items, 5, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'assetmaster/all_item.html', context)


def add_item_view(request):
    """
    This function adds new data to  Item table.

    Parameters:
    arg1 (): asset_type(str),asset_description(str)

    Returns:
    msg: 'Item Added Successfully!'

    """
    form = ItemForm()
    image_form = AssetImageForm()
    my_dict = {'form': form, 'image_form': image_form}
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=True)
            print(item.item_id)
            for file in files:
                print(file)
                AssetImage.objects.create(item_id=item, item_image=file)
            messages.success(request, 'Item Added Successfully!')
            return redirect('/all_items')
        else:
            messages.error(request, 'Something went wrong!')
            return render(request, 'assetmaster/add_item.html', my_dict)
    return render(request, 'assetmaster/add_item.html', my_dict)

def update_item_view(request, id):
    """
    This data update data from Item table.

    Parameters:
    arg1 ():
    arg2 (int): id of object

    Returns:
    msg: 'Item updated Successfully!'

    """
    item = Item.objects.get(item_id=id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated Successfully!')
            return HttpResponseRedirect('/all_items')
    else:
        form = ItemForm(instance=item)
    context = {'form': form}
    return render(request, 'assetmaster/update_item.html', context)

def remove_item_view(request, id):
    """
    This function fetch all the data from Item table.

    Parameters:
    arg1 (): HttpRequest Object
    arg2 (): uuid of Item object

    Returns:
    msg: 'Items deleted Successfully!'

    """
    if id:
        item_to_be_removed = Item.objects.get(item_id=id)
        item_to_be_removed.delete()
        messages.success(request, 'Items deleted Successfully!')

    return redirect('/all_items')

def show_images(request, id):
    if id:
        images = AssetImage.objects.filter(item_id=id)
        print(images)
        context = {'images': images}
        return render(request, 'assetmaster/item_images.html', context)

def export_items_csv(request):
    """
        This function return a CSV file of all objects of Item table.

        Parameters:
        arg1 (): HttpRequest Object

        Returns:
        file: .csv

        """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Items_list' + \
        str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['item_name', 'asset_type', 'is_active', 'created_at', 'updated_at'])
    items = Item.objects.all()
    for item in items:
        writer.writerow([item.item_name, item.asset_type, item.is_active, item.created_at, item.updated_at])

    return response


def pie_chart_view(request):
    """
        This api returns a data of number of assets as per asset type.

        Parameters:
        arg1 (): HttpRequest Object

        Returns:
        json: graph label and data

        """
    pie_label = []
    queryset = AssetType.objects.all().order_by('asset_type')
    for asset in queryset:
        pie_label.append(asset.asset_type)
    pie_data = []
    data = Item.objects.values('asset_type').order_by('asset_type').annotate(Count('asset_type'))
    for asset_count in data:
        pie_data.append(asset_count['asset_type__count'])
    data = {'title': 'Count of Asset', "pie_label": pie_label, "pie_data": pie_data}
    return JsonResponse(data)


def bar_chart_view(request):
    """
        This api returns a data of number of active assets & inactive assets..

        Parameters:
        arg1 (): HttpRequest Object

        Returns:
        json: graph labels and data

        """
    Response_data = []
    temp_dict = {}

    bar_label = ['Active Assets', 'Inactive Assets']
    item_detail = Item.objects.values('is_active').order_by().annotate(Count('item_id'))
    # for count in bdata:
    #     bar_data.append(count['item_id__count'])
    print(item_detail)
    for i in range(len(bar_label)):
         temp_dict['label']=bar_label[i]
         temp_dict['Count']=item_detail[i]['item_id__count']
         Response_data.append(temp_dict)
         temp_dict = {}
    print(Response_data)
    return JsonResponse(Response_data, safe=False)


