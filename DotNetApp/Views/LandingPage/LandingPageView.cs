using Application.ViewModels.LandingPage;
using DotNetApp.Core.Configuration;
using DotNetApp.Core.ViewConfiguration;
using DotNetApp.ViewConfigurations.LandingPage;
using System.IO;
using System.Text;
using System.Web.Mvc;
using Models = Application.ViewModels;

namespace Application.Views.LandingPage
{
    /// <summary>
    /// Landing page view component for the legacy ASP.NET MVC application.
    /// This class handles the rendering of the landing page UI elements using traditional
    /// server-side rendering approach typical in ASP.NET MVC applications.
    /// </summary>
    public class LandingPageView : BaseView<LandingPagModel>
    {
        public override string ConfigreStyles()
        {
            return "<link rel='stylesheet' href='Content/LandingPage/LandingPage.css'>";
        }

        public override string ConfigureFooterPanel()
        {
            StringBuilder footer = new StringBuilder();
            footer.AppendLine("<div class='button-group'>");
            footer.AppendLine("<button class='btn-primary' id='continue'>Continue</button><button class='btn-secondary'>Clear All</button>");
            footer.AppendLine("</div>");
            return footer.ToString();

        }

        public override string ConfigureScripts()
        {
            return "<script src='Scripts/LandingPage/LandingPage.js'/></script>";
        }

        public override PropertyConfiguration<LandingPagModel> InvokeConfiguration(LandingPagModel viewModel)
        {
            var configurations = new LandingPageConfiguration(viewModel);
            configurations.ConfigureModel();

            return configurations;
        }

        public void Render2(ViewContext viewContext, TextWriter writer)
        {
            var model = (Models.LandingPage.LandingPagModel)viewContext.ViewData.Model;

            var configurations = new LandingPageConfiguration(model);
            configurations.ConfigureModel();

            // Render the view using the configured model
            StringBuilder controls = new StringBuilder();

            // add css feature 3 column layout
            controls.AppendLine("<link rel='stylesheet' href='Content/LandingPage/LandingPage.css'>");
            int columnCount = 0;
            controls.AppendLine("<div class='overlay' onclick='closePopup('')'></div>");
            controls.AppendLine("<div class='container'><div class='header'>Initiation</div><div class='form-section'>");
            foreach (var property in configurations.GetConfigurations())
            {
               
                controls.AppendLine("<div class='form-group'>");
                string disableStr = string.Empty;
                if (property.IsDisabled)
                {
                    disableStr = "disabled";
                }
                controls.AppendLine("<label for="+property.Id+">"+property.Name+"</label>");

                if (property.Type == "textbox")
                {
                    controls.AppendLine(string.Format("<input type='text' id='{0}' name='{0}' />", property.Id));
                }
                else if (property.Type == "checkbox")
                {
                    controls.AppendLine(string.Format("<input type='checkbox' id='{0}' name='{0}' />", property.Id));
                }
                else if(property.Type == "lookup")
                {
                    controls.AppendLine("<div class='flex-group'>");
                    controls.AppendLine(string.Format("<input type='text' id='{0}' name='{0}' />", property.Id));
                    controls.AppendLine("<button onclick=openPopup('"+ property.Id.Trim() + "')>🔍</button>");
                    controls.AppendLine("</div>");
                    controls.Append("<div class='info "+ property.Id+ "'></div>");
                }
                else if(property.Type == "dropdown")
                {
                    controls.AppendLine("<select id=" + property.Id + " name='" + property.Id + "' " + disableStr + "></select>");
                }

                controls.AppendLine("</div>");
                columnCount++;
            }
            if(columnCount % 2 != 0)
            {
                controls.AppendLine("</div>");
            }           

            controls.AppendLine("<div class='button-group'>");
            controls.AppendLine("<button class='btn-primary' id='continue'>Continue</button><button class='btn-secondary'>Clear All</button>");
            controls.AppendLine("</div></div></div>");
            controls.AppendLine("<script src='Scripts/LandingPage/LandingPage.js'/></script>");
            writer.Write(controls.ToString());
        }
    }
}