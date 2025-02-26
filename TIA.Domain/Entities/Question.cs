using TIA.Domain.Common;

namespace TIA.Domain.Entities
{
    public class Question : BaseEntity
    {
        public Guid FileId { get; set; }
        public AppFile File { get; set; } = null!;
        public string Statement { get; set; } = string.Empty;
        public ICollection<Answear> Answears { get; set; } = new List<Answear>();
        public bool IsDone { get; set; }
        public bool? DoneCorrectly { get; set; }
    }
}
