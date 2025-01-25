using System;
using System.Collections.Generic;

namespace DotNetApp.Core.Configuration
{
    public abstract class Configuration
    {
        private readonly IDictionary<string, Configuration> _configurations;
        private readonly List<string> _keysInOrder;

        public string Id { get; set; }
        public string Name { get; set; }
        public string Value { get; set; }
        public string Type { get; set; }
        public bool IsRequired { get; set; }
        public bool IsDisabled { get; set; }

        public int MaxLength { get; set; }
        public int MinLength { get; set; }
        public string Pattern { get; set; }

        public Configuration()
        {
            _configurations = new Dictionary<string, Configuration>(StringComparer.OrdinalIgnoreCase);
            _keysInOrder = new List<string>();
        }

        private Configuration Add(string name, Configuration configuration)
        {
            _configurations.Add(name, configuration);
            _keysInOrder.Add(name);

            return _configurations[name];
        }

        public IEnumerable<Configuration> GetAll()
        {
            foreach (var key in _keysInOrder)
            {
                yield return _configurations[key];
            }
        }

        public abstract void ConfigureModel();
        public Configuration AddConfiguration(string name, Configuration configuration)
        {
            return Add(name, configuration);
        }

        public IEnumerable<Configuration> GetConfigurations()
        {
            return GetAll();
        }
    }
}
