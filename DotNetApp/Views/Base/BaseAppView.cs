using Application.ViewModels.ASIA.India.BKT;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.ASIA.India.BKT;
using System;
using System.Linq;

namespace DotNetApp.Views.Base
{
    public class BaseAppView<TModel, TConfiguration> : BaseView<TModel> where TModel : class where TConfiguration : PropertyConfiguration<TModel>
    {
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

        public override PropertyConfiguration<TModel> InvokeConfiguration(TModel model)
        {
            //var assemblies = AppDomain.CurrentDomain.GetAssemblies().Where(type => type.FullName.Contains("DotNetApp.ViewConfigurations")).ToList();
            //foreach (var assembly in assemblies)
            //{
            //    var configurationType = assembly.GetTypes().FirstOrDefault(type => type.FullName.Contains(typeof(TConfiguration).Name));
            //    if (configurationType != null)
            //    {
            //        var configurations = (PropertyConfiguration<TModel>)Activator.CreateInstance(configurationType, model);
            //        configurations.ConfigureModel();
            //        return configurations;
            //    }
            //}
            //return null;
            Type configurationType = typeof(TConfiguration);
            var configurations = (TConfiguration)Activator.CreateInstance(configurationType, model);
            configurations.ConfigureModel();
            return configurations;
        }
    }
}