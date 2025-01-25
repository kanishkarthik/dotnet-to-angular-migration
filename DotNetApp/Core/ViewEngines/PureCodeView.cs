using System;
using System.IO;
using System.Web.Mvc;

namespace DotNetApp.Core.ViewEngines
{
    internal class PureCodeView : IView
    {
        private string viewName;

        public PureCodeView(string viewName)
        {
            this.viewName = viewName;
        }

        public void Render(ViewContext viewContext, TextWriter writer)
        {
            Type viewType = null;
            viewType = GetViewType(viewType);

            if(viewType == null)
            {
                throw new Exception(string.Format("View not found, {0}",viewName));
            }

            var view = Activator.CreateInstance(viewType) as IView;
            view.Render(viewContext, writer);
        }

        private Type GetViewType(Type viewType)
        {
            foreach(var assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                foreach(var type in assembly.GetTypes())
                {
                    if(typeof(IView).IsAssignableFrom(type) && type.Name == this.viewName)
                    {
                        viewType = type;
                        break;
                    }
                }
            }
            return viewType;
        }
    }
}
