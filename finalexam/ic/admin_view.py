from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.timezone import now
from .models import ModelInfo

@staff_member_required
def retrain_model_view(request, model_id):
    model = get_object_or_404(ModelInfo, id=model_id)

    try:
        # Simulate retraining logic
        new_model_path = "rfc_lecturer.pkl"
        summary = "Retrained model with new data"

        model.model_file = new_model_path
        model.model_summary = summary
        model.training_date = now()
        model.save()

        messages.success(request, "Model retrained successfully.")
    except Exception as e:
        messages.error(request, f"Retraining failed: {str(e)}")

    return redirect('/admin/ic/modelinfo/')
