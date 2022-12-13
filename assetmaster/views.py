import datetime

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import AssetType,Item
from .forms import AssetTypeForm,ItemForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse,JsonResponse
import csv
# Create your views here.


@login_required(redirect_field_name='login', login_url='/account/login/')
def dashboardView(request):

    pie_label = []
    pldata = AssetType.objects.all().order_by('asset_type')
    for asset in pldata:
        pie_label.append(asset.asset_type)
    pie_data = []
    pdata = Item.objects.values('asset_type').order_by('asset_type').annotate(Count('asset_type'))
    for asset_count in pdata:
        pie_data.append(asset_count['asset_type__count'])
    print(pie_label)
    print(pie_data)

    bar_label = ['Active Assets','Inactive Assets']
    bar_data = []
    bdata = Item.objects.values('is_active').order_by().annotate(Count('item_id'))
    for count in bdata:
        bar_data.append(count['item_id__count'])
    print(bar_label)
    print(bar_data)

    data = {"bar_label": bar_label,"bar_data": bar_data,"pie_label": pie_label,"pie_data": pie_data}
    return render(request,'assetmaster/dashboard1.html',data)

def assetTypeView(request):
    assettype = AssetType.objects.all()
    context = {'assettype': assettype}
    return render(request,'assetmaster/all_assettype.html',context)


def addAssetTypeView(request):

    form = AssetTypeForm()
    my_dict = {'form': form}
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'AssetType Added Sucessfully!')
            return redirect('/all_category')
        else:
            messages.error(request, 'Something went wrong!')
            return render(request,'assetmaster/add_assettype.html',my_dict)
    return render(request,'assetmaster/add_assettype.html',my_dict)


def updateAssetTypeView(request,id):

    assettype = AssetType.objects.get(asset_type_id=id)
    if request.method == 'POST':
        form = AssetTypeForm(request.POST, instance=assettype)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assettype updated Sucessfully!')
            return HttpResponseRedirect('/all_category')
    else:
        form = AssetTypeForm(instance=assettype)
    context = {'form': form}
    return render(request, 'assetmaster/update_assettype.html',context )

def removeAssetTypeView(request,id):
    """
                                    """
    at_to_be_removed = AssetType.objects.get(asset_type_id=id)
    at_to_be_removed.delete()
    messages.success(request, 'Assettype deleted Sucessfully!')
    return redirect('/all_category')


def itemsView(request):
    items = Item.objects.all().order_by('-updated_at')
    paginator = Paginator(items, 2, orphans=1)
    page_number  = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request,'assetmaster/all_item.html', context)


def addItemView(request):

    form = ItemForm()
    my_dict = {'form': form}
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Item Added Sucessfully!')
            return redirect('/all_items')
        else:
            messages.error(request, 'Something went wrong!')
            return render(request,'assetmaster/add_item.html',my_dict)
    return render(request,'assetmaster/add_item.html',my_dict)

def updateItemView(request,id):

    item = Item.objects.get(item_id=id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated Sucessfully!')
            return HttpResponseRedirect('/all_items')
    else:
        form = ItemForm(instance=item)
    context = {'form': form}
    return render(request, 'assetmaster/update_item.html', context)

def removeItemView(request,id):

    item_to_be_removed = Item.objects.get(item_id=id)
    item_to_be_removed.delete()
    messages.success(request, 'Items deleted Sucessfully!')
    return redirect('/all_items')


def export_items_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Items_list'+ \
        str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['item_name','asset_type','is_active','created_at','updated_at'])
    items = Item.objects.all()
    for item in items:
        writer.writerow([item.item_name,item.asset_type,item.is_active,item.created_at,item.updated_at])

    return response

def pie_chart_View(request):

    pie_label = []
    pldata = AssetType.objects.all().order_by('asset_type')
    for asset in pldata:
        pie_label.append(asset.asset_type)
    pie_data = []
    pdata = Item.objects.values('asset_type').order_by('asset_type').annotate(Count('asset_type'))
    print(pdata)
    for asset_count in pdata:
        pie_data.append(asset_count['asset_type__count'])
    print(pie_label)
    print(pie_data)
    data = {'title':'Count of Asset',"pie_label": pie_label,"pie_data": pie_data}
    return JsonResponse(data)

def bar_chart_Data(request):


    bar_label = ['Active Assets','Inactive Assets']
    bar_data = []
    bdata = Item.objects.values('is_active').order_by().annotate(Count('item_id'))
    for count in bdata:
        bar_data.append(count['item_id__count'])
    ybar_label = []

    print(bar_label)
    print(bar_data)

    for i in range(0,max(bar_data) + 10, 2):
        ybar_label.append(i)
    print(ybar_label)
    data = {'title':'Asset Status',"bar_label": bar_label,"bar_data": bar_data}
    return JsonResponse(data)










    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

   """