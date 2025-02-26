using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IQuizRepository : IBaseRepository<AppFile>
    {
        Task<IEnumerable<Answear>> GetAnswersByQuestionIdAsync(Guid questionId, CancellationToken cancellationToken);
        Task<IEnumerable<Question>> GetQuestionsByQuizIdAsync(Guid fileId, CancellationToken cancellationToken);
    }
}
