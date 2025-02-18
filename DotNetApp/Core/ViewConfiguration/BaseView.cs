using DotNetApp.Core.Configuration;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Web.Mvc;

namespace DotNetApp.Core.ViewConfiguration
{
    public abstract class BaseView<TViewModel> : IView where TViewModel : class
    {
        private TextWriter _writer;
        private ViewContext _ViewContext;

        public abstract PropertyConfiguration<TViewModel> InvokeConfiguration(TViewModel viewModel);
        public abstract string ConfigureFooterPanel();
        public virtual string ConfigreStyles()
        {
            return string.Empty;
        }
        public virtual string ConfigureScripts()
        {
            return string.Empty;
        }
        public virtual void Render(ViewContext viewContext, TextWriter writer)
        {
            _writer = writer;
            _ViewContext = viewContext;
            var model = viewContext.ViewData.Model as TViewModel;
            var configurations = InvokeConfiguration(model);
            if (configurations != null)
            {
                ConfigurePanel(configurations.GetConfigurations());
            }
        }
        public void ConfigurePanel(IEnumerable<Configuration.Configuration> configurations)
        {
            // Render the view using the configured model
            StringBuilder controls = new StringBuilder();
            // add css feature 3 column layout
            controls.AppendLine(ConfigreStyles());
            int columnCount = 0;
            controls.AppendLine("<div class='overlay' onclick='closePopup('')'></div>");
            controls.AppendLine("<div class='container'><div class='header'>Initiation</div>");
            bool isPanel = false;
            isPanel = configurations.Where(x => x.Id.Contains(".")).Count() > 0;
            string panelName = string.Empty;
            if (!isPanel) { 
                controls.AppendLine("<div class='form-section'>");
            }
            foreach (var property in configurations)
            {
                if (isPanel)
                {
                    if (panelName != property.Id.Split('.')[0])
                    {
                        if (!string.IsNullOrEmpty(panelName))
                        {
                            controls.AppendLine("</div></div>");
                        }
                        panelName = property.Id.Split('.')[0];
                        controls.AppendLine("<div class='section'>");
                        string headerPanelName = Regex.Replace(panelName, "(?<!^)([A-Z])", " $1");
                        controls.AppendLine("<div class='section-header'>"+ headerPanelName + "</div>");
                        controls.AppendLine("<div class='grid-container'>");
                    }
                }

                controls.AppendLine("<div class='form-group"+ (property.Type == "lookup" ? " lookup-item" : "")+"'>");
                string disableStr = string.Empty;
                string requiredStr = string.Empty;
                if (property.IsDisabled)
                {
                    disableStr = "disabled";
                }
                if (property.IsRequired)
                {
                    requiredStr = "<span class='required'>*</span>";
                }
                controls.AppendLine("<label for=" + property.Id + ">" + property.Name + requiredStr +"</label>");
                if (property.Type == "label")
                {
                    controls.AppendLine(string.Format("<label id='{0}' name='{0}' />", property.Id));
                }
                else if (property.Type == "textbox")
                {
                    var maxLengthStr = property.MaxLength > 0 ? string.Format("maxlength={0}", property.MaxLength): "";
                    controls.AppendLine(string.Format("<input type='text' id='{0}' name='{0}' {1}/>", property.Id, maxLengthStr));
                }
                else if (property.Type == "date")
                {
                    controls.AppendLine(string.Format("<input type='date' id='{0}' name='{0}' />", property.Id));
                }
                else if (property.Type == "textarea")
                {
                    controls.AppendLine(string.Format("<textarea id='{0}' name='{0}' ></textarea>", property.Id));
                }
                else if (property.Type == "checkbox")
                {
                    controls.AppendLine(string.Format("<input type='checkbox' id='{0}' name='{0}' />", property.Id));
                }
                else if (property.Type == "lookup")
                {
                    controls.AppendLine("<div class='flex-group'>");
                    controls.AppendLine(string.Format("<input type='text' id='{0}' name='{0}' />", property.Id));
                    controls.AppendLine("<button onclick=openPopup('" + property.Id.Trim().Replace(".","_") + "')>🔍</button>");
                    controls.AppendLine("</div>");
                    controls.Append("<div class='info " + property.Id + "'></div>");
                }
                else if (property.Type == "dropdown")
                {
                    controls.AppendLine("<select id=" + property.Id + " name='" + property.Id + "' " + disableStr + "></select>");
                }

                controls.AppendLine("</div>");
                columnCount++;
            }
            if (!isPanel)
            {
                controls.AppendLine("</div>");
            }
            else
            {
                controls.AppendLine("</div></div>");
            }        
            controls.AppendLine(ConfigureFooterPanel());
            controls.AppendLine("</div></div>");
            controls.AppendLine(ConfigureScripts());
            _writer.Write(controls.ToString());

        }

    }
}
