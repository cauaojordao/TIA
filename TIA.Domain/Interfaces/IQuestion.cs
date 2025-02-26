using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IQuestion
    {
        Guid FileId { get; set; }
        AppFile File { get; set; }
        string Statement { get; set; }
        ICollection<Answear> Answears { get; set; }
        bool IsDone { get; set; }
        bool? DoneCorrectly { get; set; }
    }
}
