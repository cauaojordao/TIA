using System.ComponentModel.DataAnnotations.Schema;
using TIA.Domain.Common;

namespace TIA.Domain.Entities
{
    public class AppFile : BaseEntity
    {
        public Guid UserId { get; set; }
        public Account User { get; set; } = null!;
        public string? Folder { get; set; }
        public string Name { get; set; } = "Untitled";
        public string Summary { get; set; } = string.Empty;
        public ICollection<Question> Questions { get; set; } = new List<Question>();
        [Column(TypeName = "decimal(2,1)")]
        public decimal Efficiency { get; set; } = 0;
    }
}