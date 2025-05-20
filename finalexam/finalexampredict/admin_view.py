from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.timezone import now
from .models import ModelInfo

@staff_member_required
def retrain_model_view(requst, model_id):
    model = get_object_or_404

    try:
        new_model_path = f"models/{model.model_name.lower()}_retrained.pkl"
        summary = "retrained model with new data"

        #update model info
        model.model_file =new_model_path
        model.model_summary = summary
        model.training_date = now()
        model.save()

        messages.success(requst, "model retrained succesfully")
    except Exception as e:
        messages.error(requst, f"retraining failed: {str(e)}")
    return redirect('/admin/finalexampredict/modelinfo/')