using DotNetApp.ViewConfigurations.NAM.US.BKT;
using Application.ViewModels.NAM.US.BKT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;

namespace Application.Views.NAM.US
{
    public class USBKTView : BaseView<USBKTModel>
    {
        public override PropertyConfiguration<USBKTModel> InvokeConfiguration(USBKTModel model)
        {
            var configurations = new USBKTConfiguration(model);
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