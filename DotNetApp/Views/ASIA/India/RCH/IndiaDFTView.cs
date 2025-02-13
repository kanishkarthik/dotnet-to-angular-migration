using Application.ViewModels.ASIA.India.RCH;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.ASIA.India.RCH;

namespace Application.Views.ASIA.India.RCH
{
    public class IndiaRCHView : BaseView<IndiaRCHModel>
    {
        public override PropertyConfiguration<IndiaRCHModel> InvokeConfiguration(IndiaRCHModel model)
        {
            var configurations = new IndiaRCHConfiguration(model);
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
