using Application.ViewModels.ASIA.India.BKT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.ASIA.India.BKT;

namespace Application.Views.ASIA.India.BKT
{
    public class IndiaBKTView : BaseView<IndiaBKTModel>
    {
        public override PropertyConfiguration<IndiaBKTModel> InvokeConfiguration(IndiaBKTModel model)
        {
            var configurations = new IndiaBKTConfiguration(model);
            configurations.ConfigureModel();

            return configurations;
        }

        public override string ConfigreStyles()
        {
            return "<link rel='stylesheet' href='Content/Initiation/Initiation.css'>";
        }

        public override string ConfigureScripts()
        {
            return "<script src='Scripts/Initiation/Initiation.js'/></script>";
        }
        public override string ConfigureFooterPanel()
        {
            return $"<div class='actions'> <button class='primary'>Submit</button><button class='secondary'>Cancel</button></div>";
        }

    }
}